import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ChatType

router = Router()

KEYWORDS = {
    "Gamma♻️": "https://cutt.ly/JrwFGuLV",
    "Daddy♻️": "https://cutt.ly/3rwFGk4S",
    "R7🫥": "https://cutt.ly/WrwFGmIF",
    "Kent👀": "https://cutt.ly/frwFGIgw",
    "Аркада👾": "https://cutt.ly/prwFGGrU",
    "Catcasino🐱": "https://cutt.ly/zrwFGCwp",
    "Kometa☄️": "https://cutt.ly/CrwFG01w",
}


@router.message(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
async def keyword_handler(message: Message):
    text = message.text
    for keyword, link in KEYWORDS.items():
        if keyword in text:
            await message.reply(f"🔗 Ваша ссылка: {link}")
            break
