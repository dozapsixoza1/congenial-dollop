import asyncio
import random
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database import (
    get_or_create_user, is_banned, update_game_stats,
    update_user_xp, give_achievement, get_user
)
from translations import t, get_user_lang
from config import (
    MIN_PLAYERS, MAX_PLAYERS, GAME_JOIN_TIMEOUT, DISCUSSION_TIME,
    VOTE_TIME, NIGHT_TIME, ROLES_DISTRIBUTION, ROLE_EMOJIS,
    XP_WIN, XP_LOSE, XP_KILL, XP_SURVIVE_ROUND
)

router = Router()

# Active games storage: {chat_id: GameState}
active_games = {}

ROLE_DESCRIPTIONS = {
    "citizen": {
        "ru": "Ты мирный житель. Голосуй и помогай найти мафию!",
        "en": "You are a citizen. Vote and help find the mafia!",
        "am": "Դու քաղաքացի ես: Ձայնատուր և օգնիր գտնել մաֆիան:"
    },
    "mafia": {
        "ru": "Ты мафия! Убивай ночью, не раскрывайся днём.",
        "en": "You are Mafia! Kill at night, stay hidden during the day.",
        "am": "Դու մաֆիա ես! Գիշերով սպանիր, ցերեկով թաքնվիր:"
    },
    "godfather": {
        "ru": "Ты Крёстный Отец! Глава мафии. Детектив не может тебя раскрыть.",
        "en": "You are the Godfather! Mafia boss. The detective can't identify you.",
        "am": "Դու Կնքահայրն ես! Մաֆիայի առաջնորդ: Դետեկտիվը չի կարող բացահայտել:"
    },
    "detective": {
        "ru": "Ты детектив! Каждую ночь можешь проверить роль одного игрока.",
        "en": "You are the Detective! Each night you can check one player's role.",
        "am": "Դու դետեկտիվ ես! Ամեն գիշեր կարող ես ստուգել մեկ խաղացողի դերը:"
    },
    "doctor": {
        "ru": "Ты доктор! Каждую ночь можешь вылечить одного игрока (в т.ч. себя).",
        "en": "You are the Doctor! Each night you can heal one player (including yourself).",
        "am": "Դու բժիշկ ես! Ամեն գիշեր կարող ես բժշկել մեկ խաղացողի:"
    },
    "maniac": {
        "ru": "Ты маньяк! Убиваешь одиночку каждую ночь. Побеждаешь один.",
        "en": "You are the Maniac! Kill solo each night. You win alone.",
        "am": "Դու մոլագար ես! Ամեն գիշեր սպանիր: Հաղթում ես մենակ:"
    },
    "prostitute": {
        "ru": "Ты проститутка! Каждую ночь можешь заблокировать действие игрока.",
        "en": "You are the Prostitute! Each night you can block a player's action.",
        "am": "Դու պոռնիկ ես! Ամեն գիշեր կարող ես արգելափակել խաղացողի գործողությունը:"
    },
    "bodyguard": {
        "ru": "Ты телохранитель! Защищаешь игрока ночью. Если на него напасть — ты убиваешь нападавшего.",
        "en": "You are the Bodyguard! Protect a player at night. If attacked, you kill the attacker.",
        "am": "Դու թիկնազոր ես! Գիշերով պաշտպանիր: Հարձակման դեպքում սպանիր հարձակվողին:"
    },
    "sheriff": {
        "ru": "Ты шериф! Можешь застрелить одного игрока днём (одноразово).",
        "en": "You are the Sheriff! You can shoot one player during the day (once).",
        "am": "Դու շերիֆ ես! Ցերեկով կարող ես կրակել մեկ խաղացողի:"
    },
    "spy": {
        "ru": "Ты шпион! Каждую ночь видишь, кого мафия собирается убить.",
        "en": "You are the Spy! Each night you see who the mafia targets.",
        "am": "Դու լրտես ես! Ամեն գիշեր տեսնում ես, թե մաֆիան ում է թիրախավ:"
    },
    "bomber": {
        "ru": "Ты бомбист! При изгнании взрываешься и убираешь соседей по кругу.",
        "en": "You are the Bomber! When eliminated, you explode and kill your neighbors.",
        "am": "Դու ռմբարկու ես! Հեռացման ժամանակ պայթիր և սպանիր հարեւաններին:"
    },
    "journalist": {
        "ru": "Ты журналист! Раз в игру можешь раскрыть роль одного игрока всем.",
        "en": "You are the Journalist! Once per game, reveal one player's role to all.",
        "am": "Դու լրագրող ես! Մեկ անգամ կարող ես բացահայտել մեկ խաղացողի դերը:"
    },
}

class GameState:
    def __init__(self, chat_id, started_by):
        self.chat_id = chat_id
        self.started_by = started_by
        self.players = {}  # user_id: {name, role, alive, kills}
        self.phase = "waiting"  # waiting, night, day, voting
        self.round = 0
        self.night_actions = {}
        self.votes = {}
        self.doctor_heal = None
        self.prostitute_block = None
        self.journalist_used = False
        self.sheriff_used = False

    def add_player(self, user_id, name):
        self.players[user_id] = {
            "name": name, "role": None, "alive": True, "kills": 0
        }

    def remove_player(self, user_id):
        self.players.pop(user_id, None)

    def alive_players(self):
        return {uid: p for uid, p in self.players.items() if p["alive"]}

    def assign_roles(self):
        count = len(self.players)
        # Find closest distribution
        sizes = sorted(ROLES_DISTRIBUTION.keys())
        best = sizes[0]
        for s in sizes:
            if s <= count:
                best = s
        dist = ROLES_DISTRIBUTION[best]
        roles = []
        for role, num in dist.items():
            roles.extend([role] * num)
        # Fill remaining with citizens
        while len(roles) < count:
            roles.append("citizen")
        random.shuffle(roles)
        for uid, role in zip(self.players.keys(), roles):
            self.players[uid]["role"] = role

    def mafia_count(self):
        return sum(1 for p in self.alive_players().values()
                   if p["role"] in ["mafia", "godfather"])

    def citizen_count(self):
        return sum(1 for p in self.alive_players().values()
                   if p["role"] not in ["mafia", "godfather", "maniac"])

    def maniac_alive(self):
        return any(p["role"] == "maniac" for p in self.alive_players().values())

    def check_winner(self):
        alive = self.alive_players()
        mafia = self.mafia_count()
        citizens = self.citizen_count()
        maniac = self.maniac_alive()
        if maniac and len(alive) <= 2:
            return "maniac"
        if mafia == 0 and not maniac:
            return "citizens"
        if mafia >= citizens:
            return "mafia"
        return None

def join_game_kb(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text=t("join_game", lang), callback_data="game_join")
    kb.button(text=t("leave_game", lang), callback_data="game_leave")
    kb.button(text="🚀 Start Now", callback_data="game_force_start")
    kb.adjust(2, 1)
    return kb.as_markup()

def vote_kb(game: GameState):
    kb = InlineKeyboardBuilder()
    for uid, p in game.alive_players().items():
        kb.button(text=f"{p['name']}", callback_data=f"vote_{uid}")
    kb.button(text="🚫 Skip", callback_data="vote_skip")
    kb.adjust(2)
    return kb.as_markup()

def night_action_kb(game: GameState, exclude_uid=None):
    kb = InlineKeyboardBuilder()
    for uid, p in game.alive_players().items():
        if uid != exclude_uid:
            kb.button(text=f"{p['name']}", callback_data=f"night_{uid}")
    kb.adjust(2)
    return kb.as_markup()

@router.message(Command("startgame"))
@router.message(F.text.func(lambda x: x in ["🎮 Игра", "🎮 Game", "🎮 Խաղ"]))
async def cmd_start_game(message: Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    lang = get_user_lang(user)

    if is_banned(message.from_user.id):
        return await message.answer("🚫 You are banned.")

    chat_id = message.chat.id
    if chat_id in active_games:
        return await message.answer("⚠️ A game is already running in this chat!")

    game = GameState(chat_id, message.from_user.id)
    game.add_player(message.from_user.id, message.from_user.first_name)
    active_games[chat_id] = game

    await message.answer(
        f"🎲 <b>HarshMafia Game!</b>\n\n"
        f"👤 Players: 1\n"
        f"⏳ Joining open for {GAME_JOIN_TIMEOUT} seconds!\n\n"
        f"Tap <b>Join</b> to enter the game!",
        parse_mode="HTML",
        reply_markup=join_game_kb(lang)
    )

    asyncio.create_task(auto_start_game(message, chat_id, GAME_JOIN_TIMEOUT))

async def auto_start_game(message: Message, chat_id: int, timeout: int):
    await asyncio.sleep(timeout)
    if chat_id not in active_games:
        return
    game = active_games[chat_id]
    if game.phase != "waiting":
        return
    if len(game.players) < MIN_PLAYERS:
        await message.bot.send_message(
            chat_id,
            f"❌ Game cancelled — not enough players! (need {MIN_PLAYERS})"
        )
        active_games.pop(chat_id, None)
        return
    await begin_game(message.bot, chat_id)

@router.callback_query(F.data == "game_join")
async def cb_join(callback: CallbackQuery):
    user = get_or_create_user(callback.from_user.id, callback.from_user.username, callback.from_user.first_name)
    if is_banned(callback.from_user.id):
        return await callback.answer("🚫 You are banned!", show_alert=True)

    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return await callback.answer("No active game.", show_alert=True)
    game = active_games[chat_id]
    if game.phase != "waiting":
        return await callback.answer("Game already started!", show_alert=True)
    if callback.from_user.id in game.players:
        return await callback.answer("You're already in!", show_alert=True)
    if len(game.players) >= MAX_PLAYERS:
        return await callback.answer("Game is full!", show_alert=True)

    game.add_player(callback.from_user.id, callback.from_user.first_name)
    count = len(game.players)
    await callback.answer(f"✅ Joined! Players: {count}")
    await callback.message.edit_text(
        f"🎲 <b>HarshMafia Game!</b>\n\n"
        f"👥 Players ({count}):\n" +
        "\n".join(f"• {p['name']}" for p in game.players.values()) +
        f"\n\n⏳ Game starts automatically or when enough join!",
        parse_mode="HTML",
        reply_markup=join_game_kb(get_user_lang(user))
    )

@router.callback_query(F.data == "game_leave")
async def cb_leave(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return await callback.answer("No active game.", show_alert=True)
    game = active_games[chat_id]
    if callback.from_user.id not in game.players:
        return await callback.answer("You're not in the game.", show_alert=True)
    game.remove_player(callback.from_user.id)
    await callback.answer("❌ You left the game.")

@router.callback_query(F.data == "game_force_start")
async def cb_force_start(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return await callback.answer("No active game.", show_alert=True)
    game = active_games[chat_id]
    if callback.from_user.id != game.started_by:
        return await callback.answer("Only the host can force start!", show_alert=True)
    if len(game.players) < MIN_PLAYERS:
        return await callback.answer(f"Need at least {MIN_PLAYERS} players!", show_alert=True)
    await callback.answer("🚀 Starting!")
    await begin_game(callback.bot, chat_id)

async def begin_game(bot, chat_id):
    if chat_id not in active_games:
        return
    game = active_games[chat_id]
    game.phase = "started"
    game.assign_roles()

    count = len(game.players)
    await bot.send_message(
        chat_id,
        f"🚀 <b>Game starts!</b> Players: {count}\n\n"
        f"📨 Check your private messages for your role!",
        parse_mode="HTML"
    )

    # Send roles privately
    for uid, pdata in game.players.items():
        role = pdata["role"]
        emoji = ROLE_EMOJIS.get(role, "❓")
        desc_map = ROLE_DESCRIPTIONS.get(role, {})
        desc = desc_map.get("ru", desc_map.get("en", ""))
        try:
            await bot.send_message(
                uid,
                f"🎭 <b>Your role: {role.upper()}</b> {emoji}\n\n{desc}\n\n"
                f"🎮 Game in: {chat_id}",
                parse_mode="HTML"
            )
        except Exception:
            pass

    await asyncio.sleep(5)
    await run_night(bot, chat_id)

async def run_night(bot, chat_id):
    if chat_id not in active_games:
        return
    game = active_games[chat_id]
    game.phase = "night"
    game.round += 1
    game.night_actions = {}
    game.doctor_heal = None
    game.prostitute_block = None

    alive = game.alive_players()
    players_list = "\n".join(f"• {p['name']}" for p in alive.values())

    await bot.send_message(
        chat_id,
        f"🌙 <b>Night {game.round}</b>\n\n"
        f"👥 Alive players ({len(alive)}):\n{players_list}\n\n"
        f"💤 Everyone sleeps... Night actions sent to roles!",
        parse_mode="HTML"
    )

    # Send night action requests to special roles
    for uid, pdata in alive.items():
        role = pdata["role"]
        if role in ["mafia", "godfather"]:
            kb = night_action_kb(game, exclude_uid=uid)
            try:
                await bot.send_message(
                    uid,
                    f"🔫 <b>Mafia Night Action</b>\nChoose who to KILL:",
                    parse_mode="HTML", reply_markup=kb
                )
            except Exception:
                pass
        elif role == "detective":
            kb = night_action_kb(game, exclude_uid=uid)
            try:
                await bot.send_message(uid, "🔍 <b>Detective</b>\nChoose who to CHECK:", parse_mode="HTML", reply_markup=kb)
            except Exception:
                pass
        elif role == "doctor":
            kb = night_action_kb(game)
            try:
                await bot.send_message(uid, "💊 <b>Doctor</b>\nChoose who to HEAL:", parse_mode="HTML", reply_markup=kb)
            except Exception:
                pass
        elif role == "maniac":
            kb = night_action_kb(game, exclude_uid=uid)
            try:
                await bot.send_message(uid, "🔪 <b>Maniac</b>\nChoose who to KILL:", parse_mode="HTML", reply_markup=kb)
            except Exception:
                pass

    await asyncio.sleep(NIGHT_TIME)
    await process_night_results(bot, chat_id)

async def process_night_results(bot, chat_id):
    if chat_id not in active_games:
        return
    game = active_games[chat_id]

    killed = []
    mafia_target = game.night_actions.get("mafia_kill")
    if mafia_target and mafia_target != game.doctor_heal:
        if mafia_target in game.players and game.players[mafia_target]["alive"]:
            game.players[mafia_target]["alive"] = False
            killed.append(game.players[mafia_target]["name"])

    maniac_target = game.night_actions.get("maniac_kill")
    if maniac_target and maniac_target != game.doctor_heal:
        if maniac_target in game.players and game.players[maniac_target]["alive"]:
            game.players[maniac_target]["alive"] = False
            killed.append(game.players[maniac_target]["name"])

    if killed:
        text = "☀️ <b>Morning comes!</b>\n\n💀 Killed during the night:\n" + "\n".join(f"• {n}" for n in killed)
    else:
        text = "☀️ <b>Morning comes!</b>\n\n🎉 Nobody was killed last night!"

    await bot.send_message(chat_id, text, parse_mode="HTML")

    winner = game.check_winner()
    if winner:
        await end_game(bot, chat_id, winner)
        return

    await run_day(bot, chat_id)

async def run_day(bot, chat_id):
    if chat_id not in active_games:
        return
    game = active_games[chat_id]
    game.phase = "day"
    game.votes = {}

    alive = game.alive_players()
    players_list = "\n".join(f"• {p['name']}" for p in alive.values())

    await bot.send_message(
        chat_id,
        f"💬 <b>Day {game.round} — Discussion!</b>\n\n"
        f"👥 Alive ({len(alive)}):\n{players_list}\n\n"
        f"⏳ You have {DISCUSSION_TIME} seconds to discuss!",
        parse_mode="HTML"
    )
    await asyncio.sleep(DISCUSSION_TIME)

    # Voting phase
    game.phase = "voting"
    await bot.send_message(
        chat_id,
        f"🗳️ <b>Voting Time!</b>\n\nWho should be eliminated?\n⏳ {VOTE_TIME} seconds!",
        parse_mode="HTML",
        reply_markup=vote_kb(game)
    )
    await asyncio.sleep(VOTE_TIME)
    await process_votes(bot, chat_id)

@router.callback_query(F.data.startswith("vote_"))
async def cb_vote(callback: CallbackQuery):
    chat_id = callback.message.chat.id
    if chat_id not in active_games:
        return await callback.answer("No active game.", show_alert=True)
    game = active_games[chat_id]
    if game.phase != "voting":
        return await callback.answer("Not voting phase!", show_alert=True)
    if callback.from_user.id not in game.alive_players():
        return await callback.answer("You're dead!", show_alert=True)
    if callback.from_user.id in game.votes:
        return await callback.answer("You already voted!", show_alert=True)

    target = callback.data.replace("vote_", "")
    if target == "skip":
        game.votes[callback.from_user.id] = None
        await callback.answer("🚫 Skipped vote!")
    else:
        target_id = int(target)
        game.votes[callback.from_user.id] = target_id
        target_name = game.players.get(target_id, {}).get("name", "?")
        await callback.answer(f"✅ Voted for {target_name}!")

@router.callback_query(F.data.startswith("night_"))
async def cb_night_action(callback: CallbackQuery):
    # Find game where user is a player
    target_id = int(callback.data.replace("night_", ""))
    voter_id = callback.from_user.id

    for chat_id, game in active_games.items():
        if voter_id in game.players and game.phase == "night":
            role = game.players[voter_id]["role"]
            if role in ["mafia", "godfather"]:
                game.night_actions["mafia_kill"] = target_id
                await callback.answer(f"🔫 Target set!")
            elif role == "detective":
                target_role = game.players.get(target_id, {}).get("role", "?")
                # Godfather appears as citizen
                shown_role = "citizen" if target_role == "godfather" else target_role
                try:
                    await callback.bot.send_message(
                        voter_id,
                        f"🔍 <b>Detective Result</b>\n\n{game.players[target_id]['name']} is: <b>{shown_role.upper()}</b> {ROLE_EMOJIS.get(shown_role, '')}",
                        parse_mode="HTML"
                    )
                except Exception:
                    pass
                await callback.answer("🔍 Checked!")
            elif role == "doctor":
                game.doctor_heal = target_id
                await callback.answer("💊 Healing target set!")
            elif role == "maniac":
                game.night_actions["maniac_kill"] = target_id
                await callback.answer("🔪 Kill target set!")
            return
    await callback.answer("No active game found.", show_alert=True)

async def process_votes(bot, chat_id):
    if chat_id not in active_games:
        return
    game = active_games[chat_id]

    vote_count = {}
    for voter, target in game.votes.items():
        if target:
            vote_count[target] = vote_count.get(target, 0) + 1

    eliminated = None
    if vote_count:
        max_votes = max(vote_count.values())
        top = [uid for uid, v in vote_count.items() if v == max_votes]
        if len(top) == 1:
            eliminated = top[0]

    if eliminated and eliminated in game.players:
        pdata = game.players[eliminated]
        pdata["alive"] = False
        role = pdata["role"]
        emoji = ROLE_EMOJIS.get(role, "")

        elim_text = f"💀 <b>{pdata['name']}</b> was eliminated!\nThey were: <b>{role.upper()}</b> {emoji}"

        # Bomber explodes
        if role == "bomber":
            alive_list = list(game.alive_players().keys())
            idx = list(game.players.keys()).index(eliminated)
            neighbors = []
            all_ids = list(game.players.keys())
            for offset in [-1, 1]:
                ni = (idx + offset) % len(all_ids)
                nid = all_ids[ni]
                if nid in game.alive_players():
                    game.players[nid]["alive"] = False
                    neighbors.append(game.players[nid]["name"])
            if neighbors:
                elim_text += f"\n💣 <b>EXPLOSION!</b> Also killed: {', '.join(neighbors)}"

        await bot.send_message(chat_id, elim_text, parse_mode="HTML")
    else:
        await bot.send_message(chat_id, "🗳️ No one was eliminated (tie or no votes).", parse_mode="HTML")

    winner = game.check_winner()
    if winner:
        await end_game(bot, chat_id, winner)
    else:
        await run_night(bot, chat_id)

async def end_game(bot, chat_id, winner):
    if chat_id not in active_games:
        return
    game = active_games.pop(chat_id)

    winner_texts = {
        "mafia": "🔫 <b>MAFIA WINS!</b> 🔫\n\nThe city falls to darkness...",
        "citizens": "👥 <b>CITIZENS WIN!</b> 👥\n\nJustice prevails!",
        "maniac": "🔪 <b>THE MANIAC WINS!</b> 🔪\n\nEvil walks alone...",
    }

    roles_reveal = "\n".join(
        f"{'💀' if not p['alive'] else '✅'} {p['name']}: <b>{p['role'].upper()}</b> {ROLE_EMOJIS.get(p['role'], '')}"
        for p in game.players.values()
    )

    await bot.send_message(
        chat_id,
        f"{winner_texts.get(winner, '🏁 Game Over!')}\n\n"
        f"🎭 <b>Roles Reveal:</b>\n{roles_reveal}\n\n"
        f"🔄 Start new game with /startgame",
        parse_mode="HTML"
    )

    # Update stats
    for uid, pdata in game.players.items():
        role = pdata["role"]
        won = (
            (winner == "mafia" and role in ["mafia", "godfather"]) or
            (winner == "citizens" and role not in ["mafia", "godfather", "maniac"]) or
            (winner == "maniac" and role == "maniac")
        )
        update_game_stats(uid, won, pdata.get("kills", 0))
        xp = XP_WIN if won else XP_LOSE
        update_user_xp(uid, xp)

        u = get_user(uid)
        if u:
            if u['games_played'] == 1:
                give_achievement(uid, "first_game")
            if u['games_won'] == 1:
                give_achievement(uid, "first_win")
            if u['games_won'] >= 25:
                give_achievement(uid, "legend")
            if u['kills'] >= 10:
                give_achievement(uid, "serial_killer")
            if u['games_played'] >= 50:
                give_achievement(uid, "veteran")

@router.message(Command("endgame"))
async def cmd_end_game(message: Message):
    from config import ADMIN_IDS
    from handlers.admin import is_admin
    if not is_admin(message.from_user.id):
        return await message.answer("❌ No permission.")
    chat_id = message.chat.id
    if chat_id not in active_games:
        return await message.answer("No active game.")
    active_games.pop(chat_id)
    await message.answer("🛑 Game forcefully ended by admin.")

@router.message(Command("gamestatus"))
async def cmd_game_status(message: Message):
    chat_id = message.chat.id
    if chat_id not in active_games:
        return await message.answer("❌ No active game in this chat.")
    game = active_games[chat_id]
    alive = game.alive_players()
    text = (
        f"📊 <b>Game Status</b>\n\n"
        f"🔄 Round: {game.round}\n"
        f"🌙 Phase: {game.phase}\n"
        f"👥 Alive: {len(alive)}/{len(game.players)}\n\n"
        f"Players:\n" + "\n".join(f"• {p['name']}" for p in alive.values())
    )
    await message.answer(text, parse_mode="HTML")
