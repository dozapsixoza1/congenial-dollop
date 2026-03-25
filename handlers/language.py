from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_or_create_user, update_user_lang
from translations import t, get_user_lang, TRANSLATIONS

router = Router()

def language_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="🇷🇺 Русский", callback_data="setlang_ru")
    kb.button(text="🇬🇧 English", callback_data="setlang_en")
    kb.button(text="🇦🇲 Հայerен", callback_data="setlang_am")
    kb.button(text="🇩🇪 Deutsch", callback_data="setlang_en")
    kb.button(text="🇫🇷 Français", callback_data="setlang_en")
    kb.button(text="🇪🇸 Español", callback_data="setlang_en")
    kb.button(text="🇹🇷 Türkçe", callback_data="setlang_en")
    kb.button(text="🇸🇦 العربية", callback_data="setlang_en")
    kb.button(text="🇨🇳 中文", callback_data="setlang_en")
    kb.button(text="🇯🇵 日本語", callback_data="setlang_en")
    kb.button(text="🇰🇷 한국어", callback_data="setlang_en")
    kb.button(text="🇮🇷 فارسی", callback_data="setlang_en")
    kb.adjust(2)
    return kb.as_markup()

@router.message(Command("language"))
@router.message(F.text.func(lambda x: x in ["🌍 Язык", "🌍 Language", "🌍 Լezou"]))
async def cmd_language(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("choose_language", lang), reply_markup=language_kb())

@router.callback_query(F.data.startswith("setlang_"))
async def cb_set_language(callback: CallbackQuery):
    lang_code = callback.data.replace("setlang_", "")
    update_user_lang(callback.from_user.id, lang_code)
    user = get_or_create_user(callback.from_user.id)
    await callback.message.edit_text(t("language_set", lang_code))
    await callback.answer("✅ Language updated!")
