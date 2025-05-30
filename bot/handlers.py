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
    "Flagman": ["Flagman", "Флагман"],
    "Vavada": ["Vavada", "вавада"],
    "Vodka": ["Vodka", "водка"],
    "Cactus": ["Cactus", "Кактус"],
    "Dragon": ["Dragon", "Драгон"],
    "Stake": ["Stake", "Cтейк"],
    "Dbbet": ["Dbbet", "Дббет"],
}

LINKS = {
    "Gamma": "https://neerenicle-street.com/s6bdfa796",
    "Daddy": "https://aeruborony.com/s1256a562",
    "R7": "https://aristocratic-hall.com/sfbca26e3",
    "Kent": "https://pamuatinat.xyz/s4e7a50ec",
    "Arcada": "https://grid-cyberlane.com/sa5612f78",
    "Catcasino": "https://catchthecatsix.com/s99591107",
    "Kometa": "https://tropical-path.com/s7670a03a",
    "Gizbo": "https://gizbo-way-eight.com/c96b9b693",
    "Irwin": "https://irwinway2.com/c7b6f58b9",
    "Lex": "https://lex-irrs01.com/c77fdd5b3",
    "1go": "https://1go-blrs10.com/cb7ac564e",
    "Monro": "https://mnr-irrs12.com/c8409e923",
    "Drip": "https://drp-blrs21.com/c19244903",
    "Starda": "https://strd-blse21.com/cd29c4a0b",
    "Legzo": "https://gzo-blrs21.com/c4024b026",
    "Volna": "https://vln-blrs10.com/cd3267083",
    "Izzi": "https://izzi-blrs10.com/c78c2b891",
    "Jet": "https://jet-blrs10.com/c3d16e3a6",
    "Sol": "https://sol-blse10.com/c827e24aa",
    "Fresh": "https://fresh-blrs10.com/cebba1ef0",
    "Rox": "https://rox-fwuocypyjf.com/c161a9e18",
    "Flagman": "https://flagman-way-six.com/c18bf1d67",
    "Vavada": "https://partnervada.com/?promo=96c358a7-855a-4a86-9994-99a1d5fb7084&target=register",
    "Vodka": "https://vodka2.xyz/?id=10915",
    "Cactus": "https://cactus-balances.com/affiliate/c_d9b0mfuo",
    "Dragon": "https://dr8.to/xLd6Z",
    "Stake": "https://stake.com/?c=WXLe0LPv",
    "Dbbet": "https://db-bet.co/42HX4yR",
}


async def code_finder(text: str):
    WORD_TO_KEY = {word.lower(): key for key, words in KEYWORDS.items() for word in words}
    found_key = None
    for word in text.split():
        if word in WORD_TO_KEY:
            found_key = WORD_TO_KEY[word]
            break  # Найдено - выходим из цикла

    if found_key:  # Если нашли точное слово
        short_code = found_key.lower()
        link = f"https://dizel.online/{short_code}"
        return found_key, link

    # 2️⃣ Если точного совпадения нет, используем fuzzy matching
    best_match, score, key = process.extractOne(text, list(WORD_TO_KEY.keys()), scorer=fuzz.partial_ratio)

    if score >= 70:  # Учитываем только точность выше 70%
        matched_key = WORD_TO_KEY[best_match]
        short_code = matched_key.lower()
        link = f"https://dizel.online/{short_code}"
        return best_match, link


@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def keyword_handler(message: Message):
    try:
        text = message.text.lower()
        context, link = await code_finder(text)
        await message.reply(f"🎰 <b>{context}</b>: {link}")

    except Exception as e:
        logging.exception(e)
