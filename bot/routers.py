from pathlib import Path

from fastapi import APIRouter, HTTPException
from starlette.responses import RedirectResponse, HTMLResponse

from bot.loader import load_links, save_links
from bot.schemas import URLRequest
from typing import List

router = APIRouter(prefix="/links", tags=["Links"])
redirect_router = APIRouter()
WEBAPP_INDEX_PATH = Path("webapp/index.html")

@redirect_router.get("/webapp", response_class=HTMLResponse)
async def serve_webapp():
    if not WEBAPP_INDEX_PATH.exists():
        return HTMLResponse("<h1>index.html not found</h1>", status_code=404)

    return HTMLResponse(WEBAPP_INDEX_PATH.read_text(encoding="utf-8"))


@redirect_router.get("/{short_code}")
async def redirect(short_code: str):
    data = {key.lower(): value for key, value in load_links().items()}
    item = data.get(short_code.lower())
    if not item:
        raise HTTPException(404, "Not found")
    return RedirectResponse(item["url"])

@router.get("")
def get_links():
    return load_links()

@router.post("/{key}")
def add_link(key: str, body: URLRequest):
    data = load_links()
    if key in data:
        raise HTTPException(400, "Key already exists")
    data[key] = {"url": str(body.url), "keywords": [key]}
    save_links(data)
    return {"message": "Added"}


@router.patch("/{key}")
def update_link(key: str, body: URLRequest):
    data = load_links()

    if key not in data:
        raise HTTPException(404, "Not found")

    entry = data[key]

    if body.url:
        entry["url"] = str(body.url)

    if body.keywords is not None:
        entry["keywords"] = body.keywords

    if body.new_key and body.new_key != key:
        if body.new_key in data:
            raise HTTPException(400, "New key already exists")
        data[body.new_key] = entry
        del data[key]
    else:
        data[key] = entry

    save_links(data)
    return {"message": "Updated"}

@router.delete("/{key}")
def delete_link(key: str):
    data = load_links()
    if key not in data:
        raise HTTPException(404, "Not found")
    del data[key]
    save_links(data)
    return {"message": "Deleted"}