import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import common, admin, game, stats, chats, moderation, profile, language

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Register routers
    dp.include_router(common.router)
    dp.include_router(language.router)
    dp.include_router(admin.router)
    dp.include_router(moderation.router)
    dp.include_router(game.router)
    dp.include_router(stats.router)
    dp.include_router(chats.router)
    dp.include_router(profile.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
