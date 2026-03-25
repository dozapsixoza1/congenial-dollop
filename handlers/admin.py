from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import (
    get_or_create_user, ban_user, unban_user, is_banned, get_user,
    warn_user, reset_warns, set_admin, is_admin_db, get_global_stats,
    get_all_feedback, save_feedback
)
from translations import t, get_user_lang
from config import ADMIN_IDS, OWNER_ID

router = Router()

class AdminStates(StatesGroup):
    waiting_broadcast = State()
    waiting_ban_reason = State()
    waiting_unban_id = State()

def is_admin(user_id):
    return user_id in ADMIN_IDS or is_admin_db(user_id)

def admin_panel_kb(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text=t("admin_stats", lang), callback_data="admin_global_stats")
    kb.button(text=t("admin_users", lang), callback_data="admin_users")
    kb.button(text=t("admin_bans", lang), callback_data="admin_bans")
    kb.button(text=t("admin_broadcast", lang), callback_data="admin_broadcast")
    kb.button(text=t("admin_feedback", lang), callback_data="admin_feedback")
    kb.adjust(2, 2, 1)
    return kb.as_markup()

@router.message(F.text.func(lambda x: x in ["🛡️ Админ панель", "🛡️ Admin Panel", "🛡️ Ադмin Panel"]))
@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not is_admin(message.from_user.id):
        user = get_or_create_user(message.from_user.id)
        lang = get_user_lang(user)
        await message.answer(t("no_permission", lang))
        return
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("admin_panel", lang), parse_mode="HTML", reply_markup=admin_panel_kb(lang))

@router.callback_query(F.data == "admin_global_stats")
async def admin_global_stats(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("No permission!", show_alert=True)
    user = get_or_create_user(callback.from_user.id)
    lang = get_user_lang(user)
    stats = get_global_stats()
    text = t("global_stats_title", lang,
             users=stats['total_users'],
             games=stats['total_games'],
             banned=stats['banned'])
    await callback.message.edit_text(text, parse_mode="HTML", reply_markup=admin_panel_kb(lang))

@router.callback_query(F.data == "admin_broadcast")
async def admin_broadcast_ask(callback: CallbackQuery, state: FSMContext):
    if not is_admin(callback.from_user.id):
        return await callback.answer("No permission!", show_alert=True)
    user = get_or_create_user(callback.from_user.id)
    lang = get_user_lang(user)
    await callback.message.answer(t("broadcast_ask", lang))
    await state.set_state(AdminStates.waiting_broadcast)

@router.message(AdminStates.waiting_broadcast)
async def do_broadcast(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        return
    import sqlite3
    from config import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user_id FROM users WHERE is_banned=0")
    users = c.fetchall()
    conn.close()
    count = 0
    for (uid,) in users:
        try:
            await message.bot.send_message(uid, f"📢 <b>HarshMafia Announcement</b>\n\n{message.text}", parse_mode="HTML")
            count += 1
        except Exception:
            pass
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("broadcast_sent", lang, count=count))
    await state.clear()

@router.callback_query(F.data == "admin_feedback")
async def admin_view_feedback(callback: CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("No permission!", show_alert=True)
    feedbacks = get_all_feedback()
    if not feedbacks:
        await callback.message.edit_text("📝 No feedback yet.")
        return
    text = "📝 <b>Latest Feedback:</b>\n\n"
    for f in feedbacks[:10]:
        text += f"👤 ID: {f['user_id']}\n💬 {f['message']}\n📅 {f['date'][:10]}\n\n"
    await callback.message.edit_text(text, parse_mode="HTML")

# ─── BAN / UNBAN / WARN commands ──────────────────────────────────────

@router.message(Command("ban"))
async def cmd_ban(message: Message):
    if not is_admin(message.from_user.id):
        user = get_or_create_user(message.from_user.id)
        lang = get_user_lang(user)
        return await message.answer(t("no_permission", lang))

    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.answer("Usage: /ban <user_id> [reason]")

    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")

    reason = args[2] if len(args) > 2 else "No reason specified"
    ban_user(target_id, reason, message.from_user.id)

    target = get_user(target_id)
    name = target['first_name'] if target else str(target_id)
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("ban_success", lang, user=name, reason=reason))

    # Notify banned user
    try:
        await message.bot.send_message(
            target_id,
            f"🚫 You have been banned from HarshMafia Bot.\nReason: {reason}"
        )
    except Exception:
        pass

@router.message(Command("unban"))
async def cmd_unban(message: Message):
    if not is_admin(message.from_user.id):
        user = get_or_create_user(message.from_user.id)
        lang = get_user_lang(user)
        return await message.answer(t("no_permission", lang))

    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /unban <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")

    unban_user(target_id, message.from_user.id)
    target = get_user(target_id)
    name = target['first_name'] if target else str(target_id)
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("unban_success", lang, user=name))

    try:
        await message.bot.send_message(target_id, "✅ You have been unbanned from HarshMafia Bot!")
    except Exception:
        pass

@router.message(Command("warn"))
async def cmd_warn(message: Message):
    if not is_admin(message.from_user.id):
        user = get_or_create_user(message.from_user.id)
        lang = get_user_lang(user)
        return await message.answer(t("no_permission", lang))

    args = message.text.split(maxsplit=2)
    if len(args) < 2:
        return await message.answer("Usage: /warn <user_id> [reason]")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")

    reason = args[2] if len(args) > 2 else "No reason"
    count = warn_user(target_id, message.chat.id, reason, message.from_user.id)

    target = get_user(target_id)
    name = target['first_name'] if target else str(target_id)
    user = get_or_create_user(message.from_user.id)
    lang = get_user_lang(user)
    await message.answer(t("warn_success", lang, user=name, count=count, reason=reason))

    if count >= 3:
        ban_user(target_id, "Auto-ban: 3 warnings", message.from_user.id)
        await message.answer(t("warn_auto_ban", lang, user=name))

@router.message(Command("resetwarns"))
async def cmd_reset_warns(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /resetwarns <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    reset_warns(target_id)
    await message.answer(f"✅ Warns reset for user {target_id}.")

@router.message(Command("setadmin"))
async def cmd_set_admin(message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.answer("❌ Only owner can do this.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /setadmin <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    set_admin(target_id, True)
    await message.answer(f"✅ User {target_id} is now admin!")

@router.message(Command("removeadmin"))
async def cmd_remove_admin(message: Message):
    if message.from_user.id != OWNER_ID:
        return await message.answer("❌ Only owner can do this.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /removeadmin <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    set_admin(target_id, False)
    await message.answer(f"✅ Admin removed from user {target_id}.")

@router.message(Command("kick"))
async def cmd_kick(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /kick <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    try:
        await message.bot.ban_chat_member(message.chat.id, target_id)
        await message.bot.unban_chat_member(message.chat.id, target_id)
        await message.answer(f"👢 User {target_id} was kicked.")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(Command("mute"))
async def cmd_mute(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /mute <user_id> [minutes]")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    minutes = int(args[2]) if len(args) > 2 else 10
    from datetime import datetime, timedelta
    from aiogram.types import ChatPermissions
    until = datetime.now() + timedelta(minutes=minutes)
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, target_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until
        )
        await message.answer(f"🔇 User {target_id} muted for {minutes} minutes.")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(Command("unmute"))
async def cmd_unmute(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /unmute <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    from aiogram.types import ChatPermissions
    try:
        await message.bot.restrict_chat_member(
            message.chat.id, target_id,
            permissions=ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_polls=True, can_send_other_messages=True
            )
        )
        await message.answer(f"🔊 User {target_id} unmuted.")
    except Exception as e:
        await message.answer(f"❌ Error: {e}")

@router.message(Command("userinfo"))
async def cmd_userinfo(message: Message):
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    args = message.text.split()
    if len(args) < 2:
        return await message.answer("Usage: /userinfo <user_id>")
    try:
        target_id = int(args[1])
    except ValueError:
        return await message.answer("❌ Invalid user ID.")
    u = get_user(target_id)
    if not u:
        return await message.answer("❌ User not found in DB.")
    wr = round(u['games_won'] / u['games_played'] * 100) if u['games_played'] else 0
    text = (
        f"👤 <b>User Info</b>\n\n"
        f"🆔 ID: <code>{u['user_id']}</code>\n"
        f"👤 Name: {u['first_name']}\n"
        f"📛 Username: @{u['username'] or 'none'}\n"
        f"🌍 Lang: {u['lang']}\n"
        f"📈 Level: {u['level']} | XP: {u['xp']}\n"
        f"🎮 Games: {u['games_played']} | 🏆 Wins: {u['games_won']}\n"
        f"⚠️ Warns: {u['warn_count']}/3\n"
        f"🚫 Banned: {'Yes' if u['is_banned'] else 'No'}\n"
        f"🛡️ Admin: {'Yes' if u['is_admin'] else 'No'}\n"
        f"📅 Joined: {(u['joined_date'] or '')[:10]}\n"
    )
    await message.answer(text, parse_mode="HTML")
