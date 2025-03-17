from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

from bot.handlers import LINKS, code_finder

app = FastAPI()

@app.get("/{short_code}")
async def redirect(short_code: str):
    """Редиректит на оригинальный URL"""
    try:
        short_code = short_code.lower()  # Делаем ключ в нижнем регистре
        context, link = await code_finder(short_code)
        original_url = LINKS.get(context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=e)

    if original_url:
        return RedirectResponse(url=original_url)
    else:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
