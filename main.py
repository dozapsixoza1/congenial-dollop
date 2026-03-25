import sys
import os

# 1. Сначала ПРИНУДИТЕЛЬНО добавляем корень проекта в пути поиска.
# Это должно быть САМЫМ ПЕРВЫМ действием.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 2. Теперь исправляем опечатку (import с маленькой буквы) и загружаем остальное
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# 3. Теперь эти импорты сработают, так как Python уже знает, где искать translations и config
from config import BOT_TOKEN
from handlers import common, admin, game, stats, chats, moderation, profile, language

# Настройка логирования
logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Регистрация роутеров
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
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")
