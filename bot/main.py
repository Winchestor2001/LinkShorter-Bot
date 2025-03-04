from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from .database import Database
from .schemas import URLRequest

app = FastAPI()
db = Database()


@app.post("/shorten")
def shorten_url(short_code: str, link: str):
    short_code = db.create_short_url(link, short_code)
    return {"short_url": f"https://dizel.site/{short_code}"}


@app.get("/{short_code}")
def redirect(short_code: str):
    original_url = db.get_original_url(short_code)
    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
