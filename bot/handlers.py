import logging
import re

from aiogram import Router
from aiogram.enums import ChatType
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from rapidfuzz import process, fuzz

from bot.loader import load_links, ADMINS, DOMAIN

router = Router()


def get_keywords_links():
    data = load_links()
    keywords = {}
    links = {}
    for key, item in data.items():
        links[key] = item["url"]
        for word in item.get("keywords", []):
            keywords[word.lower()] = key
    return keywords, links


async def code_finder(text: str):
    text = text.lower()
    WORD_TO_KEY, LINKS = get_keywords_links()
    words = re.findall(r"\w+", text)

    for word in words:
        if word in WORD_TO_KEY:
            matched_key = WORD_TO_KEY[word]
            link = f"{DOMAIN}/{matched_key.lower()}"
            return matched_key, link

    best_match, score, _ = process.extractOne(text, list(WORD_TO_KEY.keys()), scorer=fuzz.partial_ratio)
    if score >= 70:
        matched_key = WORD_TO_KEY[best_match]
        link = f"{DOMAIN}/{matched_key.lower()}"
        return matched_key, link


@router.message(lambda msg: msg.chat.type == ChatType.PRIVATE)
async def webapp_keyboard_handler(message: Message):
    user_id = message.from_user.id

    if user_id in ADMINS:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🛠 Открыть панель",
                        web_app=WebAppInfo(url=f"{DOMAIN}/webapp")
                    )
                ]
            ],
            resize_keyboard=True
        )

        await message.answer("Добро пожаловать в панель управления 🔧", reply_markup=keyboard)


@router.message(lambda msg: msg.chat.type in [ChatType.GROUP, ChatType.SUPERGROUP])
async def keyword_handler(message: Message):
    try:
        result = await code_finder(message.text)
        if result:
            context, link = result
            await message.reply(f"🎰 <b>{context}</b>: {link}")
    except Exception as e:
        logging.exception(e)
