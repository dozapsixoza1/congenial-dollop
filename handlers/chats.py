# handlers/chats.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import CHATS
from database import get_or_create_user
from translations import get_user_lang

router = Router()

async def show_chats(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    kb = InlineKeyboardBuilder()
    for key, chat in CHATS.items():
        kb.button(text=f"{chat['emoji']} {chat['name']}", url=chat['link'])
    kb.adjust(1)
    await message.answer(
        "💬 <b>Our HarshMafia Communities!</b>\n\nJoin us and play Mafia with people from around the world 🌍",
        parse_mode="HTML",
        reply_markup=kb.as_markup()
    )
