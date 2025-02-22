import asyncio
import os
import sys

from loader import bot, dp
from handlers import router

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
