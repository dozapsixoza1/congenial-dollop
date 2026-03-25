from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import get_or_create_user, get_user, get_top_players, get_top_killers, get_user_achievements
from database import ACHIEVEMENTS_LIST
from translations import t, get_user_lang

router = Router()

class ProfileStates(StatesGroup):
    editing_bio = State()

def profile_kb(lang, user_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="🏆 Achievements", callback_data=f"achievements_{user_id}")
    kb.button(text="✏️ Edit Bio", callback_data="edit_bio")
    kb.button(text="🎮 Game Stats", callback_data=f"gamestats_{user_id}")
    kb.adjust(2, 1)
    return kb.as_markup()

def top_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text="⭐ By XP", callback_data="top_xp")
    kb.button(text="🏆 By Wins", callback_data="top_wins")
    kb.button(text="🔪 By Kills", callback_data="top_kills")
    kb.adjust(3)
    return kb.as_markup()

@router.message(Command("profile"))
@router.message(F.text.func(lambda x: x in ["👤 Профиль", "👤 Profile", "👤 Պրոֆիլ"]))
async def cmd_profile(message: Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    lang = get_user_lang(user)
    await send_profile(message, user, lang)

async def send_profile(message, user, lang):
    uid = user['user_id']
    wr = round(user['games_won'] / user['games_played'] * 100) if user['games_played'] else 0
    achievements = get_user_achievements(uid)
    ach_str = " ".join(
        ACHIEVEMENTS_LIST[a['achievement']]['emoji']
        for a in achievements
        if a['achievement'] in ACHIEVEMENTS_LIST
    ) or "None"

    text = (
        f"👤 <b>{user['first_name']}</b>\n"
        f"{'@' + user['username'] if user['username'] else ''}\n\n"
        f"📈 Level: <b>{user['level']}</b> | ⭐ XP: <b>{user['xp']}</b>\n"
        f"🎮 Games: <b>{user['games_played']}</b>\n"
        f"🏆 Wins: <b>{user['games_won']}</b> | 💀 Losses: <b>{user['games_lost']}</b>\n"
        f"📊 Win Rate: <b>{wr}%</b>\n"
        f"🔪 Kills: <b>{user['kills']}</b>\n"
        f"💰 Coins: <b>{user['coins']}</b>\n"
        f"⚠️ Warns: <b>{user['warn_count']}/3</b>\n"
        f"🏅 Achievements: {ach_str}\n"
    )
    if user.get('bio'):
        text += f"\n📝 Bio: {user['bio']}"

    await message.answer(text, parse_mode="HTML", reply_markup=profile_kb(lang, uid))

@router.callback_query(F.data.startswith("achievements_"))
async def cb_achievements(callback: CallbackQuery):
    uid = int(callback.data.split("_")[1])
    achievements = get_user_achievements(uid)
    if not achievements:
        return await callback.message.edit_text("🏅 No achievements yet! Play games to earn them.")

    text = "🏅 <b>Achievements:</b>\n\n"
    for a in achievements:
        key = a['achievement']
        if key in ACHIEVEMENTS_LIST:
            ach = ACHIEVEMENTS_LIST[key]
            text += f"{ach['emoji']} <b>{ach['name']}</b>\n{ach['desc']}\n📅 {a['date'][:10]}\n\n"

    await callback.message.edit_text(text, parse_mode="HTML")

@router.callback_query(F.data == "edit_bio")
async def cb_edit_bio(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("✏️ Send your new bio (max 200 chars):")
    await state.set_state(ProfileStates.editing_bio)

@router.message(ProfileStates.editing_bio)
async def save_bio(message: Message, state: FSMContext):
    import sqlite3
    from config import DB_PATH
    bio = message.text[:200]
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE users SET bio=? WHERE user_id=?", (bio, message.from_user.id))
    conn.commit()
    conn.close()
    await message.answer(f"✅ Bio updated: {bio}")
    await state.clear()

@router.callback_query(F.data.startswith("gamestats_"))
async def cb_gamestats(callback: CallbackQuery):
    uid = int(callback.data.split("_")[1])
    u = get_user(uid)
    if not u:
        return await callback.answer("User not found.")
    wr = round(u['games_won'] / u['games_played'] * 100) if u['games_played'] else 0
    text = (
        f"📊 <b>Game Stats — {u['first_name']}</b>\n\n"
        f"🎮 Games played: {u['games_played']}\n"
        f"🏆 Wins: {u['games_won']}\n"
        f"💀 Losses: {u['games_lost']}\n"
        f"📈 Win Rate: {wr}%\n"
        f"🔪 Total kills: {u['kills']}\n"
        f"📈 XP: {u['xp']} | Level: {u['level']}\n"
    )
    await callback.message.edit_text(text, parse_mode="HTML")

@router.message(Command("stats"))
@router.message(F.text.func(lambda x: x in ["📊 Статистика", "📊 Stats", "📊 Վիճakagr"]))
async def cmd_stats(message: Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    lang = get_user_lang(user)
    wr = round(user['games_won'] / user['games_played'] * 100) if user['games_played'] else 0
    text = (
        f"📊 <b>Your Stats</b>\n\n"
        f"{t('stats_games', lang, count=user['games_played'])}\n"
        f"{t('stats_wins', lang, wins=user['games_won'])}\n"
        f"{t('stats_losses', lang, losses=user['games_lost'])}\n"
        f"{t('stats_kills', lang, kills=user['kills'])}\n"
        f"{t('stats_xp', lang, xp=user['xp'])}\n"
        f"{t('stats_level', lang, level=user['level'])}\n"
        f"{t('stats_winrate', lang, wr=wr)}\n"
    )
    await message.answer(text, parse_mode="HTML")

@router.message(Command("top"))
@router.message(F.text.func(lambda x: x in ["🏆 Топ", "🏆 Top", "🏆 Լavaguynnner"]))
async def cmd_top(message: Message):
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(f"{t('top_players', lang)}\n\nChoose category:", parse_mode="HTML", reply_markup=top_kb())

@router.callback_query(F.data == "top_xp")
async def cb_top_xp(callback: CallbackQuery):
    players = get_top_players(10)
    text = "🏆 <b>Top Players by XP</b>\n\n"
    medals = ["🥇", "🥈", "🥉"] + ["4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, p in enumerate(players):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        name = p.get('first_name') or p.get('username') or str(p['user_id'])
        text += f"{medal} {name} — ⭐ {p['xp']} XP | Lv.{p['level']}\n"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=top_kb())

@router.callback_query(F.data == "top_wins")
async def cb_top_wins(callback: CallbackQuery):
    players = get_top_players(10)
    players.sort(key=lambda x: x['games_won'], reverse=True)
    text = "🏆 <b>Top Players by Wins</b>\n\n"
    medals = ["🥇", "🥈", "🥉"] + ["4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, p in enumerate(players):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        name = p.get('first_name') or str(p['user_id'])
        wr = round(p['games_won'] / p['games_played'] * 100) if p['games_played'] else 0
        text += f"{medal} {name} — 🏆 {p['games_won']} wins ({wr}%)\n"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=top_kb())

@router.callback_query(F.data == "top_kills")
async def cb_top_kills(callback: CallbackQuery):
    players = get_top_killers(10)
    text = "🔪 <b>Top Killers</b>\n\n"
    medals = ["🥇", "🥈", "🥉"] + ["4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
    for i, p in enumerate(players):
        medal = medals[i] if i < len(medals) else f"{i+1}."
        name = p.get('first_name') or str(p['user_id'])
        text += f"{medal} {name} — 🔪 {p['kills']} kills\n"
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=top_kb())
