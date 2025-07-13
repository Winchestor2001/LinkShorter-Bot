import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from environs import Env
import json
from pathlib import Path

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
ADMINS = list(map(int, env.list("ADMINS")))
DOMAIN = env.str("DOMAIN")

logging.basicConfig(level=logging.INFO)

DATA_FILE = Path("links_data.json")

def load_links() -> dict:
    if not DATA_FILE.exists():
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_links(data: dict) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
