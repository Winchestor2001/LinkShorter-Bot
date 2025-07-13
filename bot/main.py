from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from bot.routers import router, redirect_router

app = FastAPI()

# API роуты
app.include_router(router)
app.include_router(redirect_router)


app.add_middleware(
        CORSMiddleware,  # noqa  
        allow_origins="*",
        allow_credentials=True,
        allow_methods="*",
        allow_headers="*",
    )
