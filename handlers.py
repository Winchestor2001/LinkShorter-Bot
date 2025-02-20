import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from rapidfuzz import process, fuzz

router = Router()

KEYWORDS = {
    "Gamma": ["Gamma", "Гамма"],
    "Daddy": ["Daddy", "Дадди"],
    "R7": ["R7", "Р7"],
    "Kent": ["Kent", "Кент"],
    "Arcada": ["Arcada", "Аркада"],
    "Catcasino": ["Catcasino", "Каткасино"],
    "Kometa": ["Kometa", "Комета"],
}

LINKS = {
    "Gamma": "https://cutt.ly/JrwFGuLV",
    "Daddy": "https://cutt.ly/3rwFGk4S",
    "R7": "https://cutt.ly/WrwFGmIF",
    "Kent": "https://cutt.ly/frwFGIgw",
    "Arcada": "https://cutt.ly/prwFGGrU",
    "Catcasino": "https://cutt.ly/zrwFGCwp",
    "Kometa": "https://cutt.ly/CrwFG01w",
}

WORD_TO_KEY = {word.lower(): key for key, words in KEYWORDS.items() for word in words}


@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def keyword_handler(message: Message):
    try:
        text = message.text.lower()

        for word in text.split():
            if word in WORD_TO_KEY:
                key = WORD_TO_KEY[word]
                await message.reply(f"🎰 <b>{word}</b>: {LINKS[key]}")
                return

        best_match, score, key = process.extractOne(text, list(WORD_TO_KEY.keys()), scorer=fuzz.partial_ratio)

        if score >= 69:
            matched_key = WORD_TO_KEY[best_match]
            await message.reply(f"🎰 <b>{best_match}</b>: {LINKS[matched_key]}")

    except Exception as e:
        logging.exception(e)
