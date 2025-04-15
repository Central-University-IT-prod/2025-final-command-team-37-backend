import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import setup_handlers
from utils.utils import send_request


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode="HTML"))

    dp = Dispatcher()

    setup_handlers(dp)

    asyncio.create_task(send_request())

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
