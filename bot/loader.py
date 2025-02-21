import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()
