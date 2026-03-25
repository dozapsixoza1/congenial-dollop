import sys
import os

# Автоматически находим корень проекта и добавляем его в пути поиска
# Это исправляет ошибку "ModuleNotFoundError: No module named 'translations'"
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_path not in sys.path:
    sys.path.append(root_path)

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database import get_or_create_user, update_last_seen, is_banned, get_ban_info, save_feedback
from translations import t, get_user_lang
from config import ADMIN_IDS
import database as db

router = Router()

def main_menu(lang="ru", user_id=None):
    kb = ReplyKeyboardBuilder()
    kb.button(text=t("menu_game", lang))
    kb.button(text=t("menu_profile", lang))
    kb.button(text=t("menu_stats", lang))
    kb.button(text=t("menu_top", lang))
    kb.button(text=t("menu_chats", lang))
    kb.button(text=t("menu_help", lang))
    kb.button(text=t("menu_language", lang))
    kb.button(text=t("menu_settings", lang))
    if user_id and user_id in ADMIN_IDS:
        kb.button(text=t("menu_admin", lang))
    kb.adjust(2, 2, 2, 2, 1)
    return kb.as_markup(resize_keyboard=True)

@router.message(CommandStart())
async def cmd_start(message: Message):
    user = get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    update_last_seen(message.from_user.id)

    if is_banned(message.from_user.id):
        info = get_ban_info(message.from_user.id)
        lang = get_user_lang(user)
        await message.answer(t("banned", lang, reason=info['reason'], date=info['date'][:10]))
        return

    lang = get_user_lang(user)
    await message.answer(
        t("welcome", lang),
        parse_mode="HTML",
        reply_markup=main_menu(lang, message.from_user.id)
    )

@router.message(Command("help"))
@router.message(F.text.func(lambda t: any(t == x for x in ["❓ Помощь", "❓ Help", "❓ Օգնություն"])))
async def cmd_help(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("help_text", lang), parse_mode="HTML")

@router.message(Command("roles"))
@router.message(F.text == "🎭 Роли")
async def cmd_roles(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("roles_list", lang), parse_mode="HTML")

@router.message(Command("feedback"))
async def cmd_feedback_start(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("feedback_ask", lang))

@router.message(Command("chats"))
@router.message(F.text.func(lambda t: any(t == x for x in ["💬 Чаты", "💬 Chats", "💬 Չաթեր"])))
async def cmd_chats_menu(message: Message):
    # Импорт перенесен внутрь функции, чтобы избежать циклической ошибки (Circular Import)
    from handlers.chats import show_chats
    await show_chats(message)
