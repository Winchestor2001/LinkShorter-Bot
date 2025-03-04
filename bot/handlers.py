import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType
from rapidfuzz import process, fuzz

from database import Database

router = Router()
db = Database()

KEYWORDS = {
    "Gamma": ["Gamma", "Гамма"],
    "Daddy": ["Daddy", "Дадди"],
    "R7": ["R7", "Р7"],
    "Kent": ["Kent", "Кент"],
    "Arcada": ["Arcada", "Аркада"],
    "Catcasino": ["Catcasino", "Каткасино"],
    "Kometa": ["Kometa", "Комета"],
    "Gizbo": ["Gizbo", "Гизбо"],
    "Irwin": ["Irwin", "Ирвин"],
    "Lex": ["Lex", "Лекс"],
    "1go": ["1go", "1го"],
    "Monro": ["Monro", "Монро"],
    "Drip": ["Drip", "Дрип"],
    "Starda": ["Starda", "Старда"],
    "Legzo": ["Legzo", "Легзо"],
    "Volna": ["Volna", "Волна"],
    "Izzi": ["Izzi", "Иззи"],
    "Jet": ["Jet", "Джет"],
    "Sol": ["Sol", "Сол"],
    "Fresh": ["Fresh", "Фреш"],
    "Rox": ["Rox", "Рокс"],
}

LINKS = {
    "Gamma": "https://cleellbert.com/s6bdfa796",
    "Daddy": "https://nice-road-five.com/s1256a562",
    "R7": "https://aristocratic-hall.com/sfbca26e3",
    "Kent": "https://passage-through-deserts.com/s4e7a50ec",
    "Arcada": "https://synthed-neonway.com/sa5612f78",
    "Catcasino": "https://catchthecatsix.com/s99591107",
    "Kometa": "https://spangle-flight.com/s7670a03a",
    "Gizbo": "https://gizbo-way-eight.com/c96b9b693",
    "Irwin": "https://rwn-irrs01.com/c7b6f58b9",
    "Lex": "https://lex-irrs01.com/c77fdd5b3",
    "1go": "https://1go-irrs01.com/cb7ac564e",
    "Monro": "https://mnr-irrs12.com/c8409e923",
    "Drip": "https://drp-irrs12.com/c19244903",
    "Starda": "https://strd-irrs12.com/cd29c4a0b",
    "Legzo": "https://gzo-irrs01.com/c4024b026",
    "Volna": "https://vln-irrs01.com/cd3267083",
    "Izzi": "https://izzi-irrs01.com/c78c2b891",
    "Jet": "https://jetb-intsemed2.com/c3d16e3a6",
    "Sol": "https://sol-diamew02.com/c827e24aa",
    "Fresh": "https://fresh-sfgjhyrt02.com/cebba1ef0",
    "Rox": "https://rox-fwuocypyjf.com/c161a9e18",
}

WORD_TO_KEY = {word.lower(): key for key, words in KEYWORDS.items() for word in words}


@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def keyword_handler(message: Message):
    try:
        text = message.text.lower()

        # 1️⃣ Проверяем точное совпадение в `WORD_TO_KEY`
        found_key = None
        for word in text.split():
            if word in WORD_TO_KEY:
                found_key = WORD_TO_KEY[word]
                break

        if found_key:
            short_code = found_key.lower()
            existing_link = db.get_original_url(short_code)

            if existing_link:
                link = f"https://dizel.site/{short_code}"
            else:
                db.create_short_url(LINKS[found_key], short_code)
                link = f"https://dizel.site/{short_code}"

            await message.reply(f"🎰 <b>{found_key}</b>: {link}")
            return

        # 2️⃣ Если точного совпадения нет, ищем похожее слово
        best_match, score, key = process.extractOne(text, list(WORD_TO_KEY.keys()), scorer=fuzz.partial_ratio)

        if score >= 70:
            matched_key = WORD_TO_KEY[best_match]
            short_code = matched_key.lower()
            existing_link = db.get_original_url(short_code)

            if existing_link:
                link = f"https://dizel.site/{short_code}"
            else:
                db.create_short_url(LINKS[matched_key], short_code)
                link = f"https://dizel.site/{short_code}"

            await message.reply(f"🎰 <b>{best_match}</b>: {link}")

    except Exception as e:
        logging.exception(e)
