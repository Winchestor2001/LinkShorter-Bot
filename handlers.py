import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from rapidfuzz import process, fuzz

router = Router()

# https://cutt.ly
KEYWORDS = {
    "Gamma": "https://cutt.ly/JrwFGuLV",
    "Гамма": "https://cutt.ly/JrwFGuLV",

    "Daddy": "https://cutt.ly/3rwFGk4S",
    "Дадди": "https://cutt.ly/3rwFGk4S",

    "R7": "https://cutt.ly/WrwFGmIF",
    "Р7": "https://cutt.ly/WrwFGmIF",

    "Kent": "https://cutt.ly/frwFGIgw",
    "Кент": "https://cutt.ly/frwFGIgw",

    "Arcada": "https://cutt.ly/prwFGGrU",
    "Аркада": "https://cutt.ly/prwFGGrU",

    "Catcasino": "https://cutt.ly/zrwFGCwp",
    "Каткасино": "https://cutt.ly/zrwFGCwp",

    "Kometa": "https://cutt.ly/CrwFG01w",
    "Комета": "https://cutt.ly/CrwFG01w",

}


@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def keyword_handler(message: Message):
    try:
        text = message.text.lower()

        best_match, score, key = process.extractOne(text, KEYWORDS.keys(), scorer=fuzz.partial_ratio)
        if score >= 50:
            await message.reply(f"🎰 <b>{best_match}</b>: {KEYWORDS[best_match]}")
    except Exception as e:
        logging.exception(e)