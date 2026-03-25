# translations.py — Full multilingual support

TRANSLATIONS = {
    "ru": {
        "welcome": "👋 Добро пожаловать в <b>HarshMafia Bot</b>!\n\nЯ помогу тебе сыграть в Мафию прямо в Telegram!\n\nИспользуй меню ниже 👇",
        "menu_game": "🎮 Игра",
        "menu_profile": "👤 Профиль",
        "menu_stats": "📊 Статистика",
        "menu_chats": "💬 Чаты",
        "menu_top": "🏆 Топ",
        "menu_help": "❓ Помощь",
        "menu_settings": "⚙️ Настройки",
        "menu_language": "🌍 Язык",
        "menu_admin": "🛡️ Админ панель",
        "start_game": "🎮 Начать игру",
        "join_game": "✅ Присоединиться",
        "leave_game": "❌ Выйти",
        "game_started": "🎲 Игра началась! Регистрация открыта {timeout} секунд.",
        "game_begin": "🚀 Игра начинается! Игроков: {count}",
        "role_assigned": "🎭 Твоя роль: <b>{role}</b> {emoji}\n\n{description}",
        "night_begins": "🌙 <b>Наступает ночь...</b>",
        "day_begins": "☀️ <b>Наступает день!</b>",
        "discussion": "💬 Обсуждение! У вас {time} секунд.",
        "vote_time": "🗳️ Голосование! Кого изгнать?",
        "player_eliminated": "💀 {name} был изгнан! Он был: <b>{role}</b>",
        "mafia_wins": "🔫 <b>Мафия победила!</b>",
        "citizens_win": "👥 <b>Мирные победили!</b>",
        "not_enough_players": "❌ Недостаточно игроков! Минимум {min}.",
        "already_in_game": "⚠️ Ты уже в игре!",
        "game_not_found": "❌ Игра не найдена.",
        "profile_title": "👤 <b>Профиль {name}</b>",
        "stats_games": "🎮 Игр сыграно: <b>{count}</b>",
        "stats_wins": "🏆 Побед: <b>{wins}</b>",
        "stats_losses": "💀 Поражений: <b>{losses}</b>",
        "stats_kills": "🔪 Убийств: <b>{kills}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        "stats_level": "📈 Уровень: <b>{level}</b>",
        "stats_winrate": "📊 Винрейт: <b>{wr}%</b>",
        "top_players": "🏆 <b>Топ игроков</b>",
        "banned": "🚫 Ты забанен!\nПричина: {reason}\nДата: {date}",
        "ban_success": "🚫 Пользователь {user} забанен!\nПричина: {reason}",
        "unban_success": "✅ Пользователь {user} разбанен!",
        "warn_success": "⚠️ Пользователь {user} получил предупреждение ({count}/3)\nПричина: {reason}",
        "warn_auto_ban": "🚫 Пользователь {user} автоматически забанен (3 предупреждения)!",
        "no_permission": "❌ У тебя нет прав!",
        "chats_title": "💬 <b>Наши чаты HarshMafia</b>",
        "help_title": "❓ <b>Помощь</b>",
        "help_text": (
            "🎮 <b>Команды игры:</b>\n"
            "/startgame — начать игру\n"
            "/join — присоединиться\n"
            "/leave — выйти\n"
            "/roles — список ролей\n\n"
            "👤 <b>Профиль:</b>\n"
            "/profile — твой профиль\n"
            "/stats — статистика\n"
            "/top — топ игроков\n\n"
            "🛡️ <b>Модерация (только админы):</b>\n"
            "/ban — забанить\n"
            "/unban — разбанить\n"
            "/warn — предупреждение\n"
            "/kick — кикнуть\n"
            "/mute — замутить\n\n"
            "⚙️ <b>Прочее:</b>\n"
            "/language — сменить язык\n"
            "/feedback — отправить отзыв\n"
            "/chats — наши чаты\n"
        ),
        "roles_list": (
            "🎭 <b>Роли в игре:</b>\n\n"
            "👤 <b>Мирный житель</b> — голосует и вычисляет мафию\n"
            "🔫 <b>Мафия</b> — убивает ночью\n"
            "🎩 <b>Крёстный отец</b> — глава мафии, невидим для детектива\n"
            "🔍 <b>Детектив</b> — проверяет роль игрока ночью\n"
            "💊 <b>Доктор</b> — лечит игрока ночью\n"
            "🛡️ <b>Телохранитель</b> — защищает и убивает нападавшего\n"
            "🔪 <b>Маньяк</b> — убивает один, побеждает в одиночку\n"
            "💃 <b>Проститутка</b> — блокирует действие игрока\n"
            "⭐ <b>Шериф</b> — может убить одного игрока днём\n"
            "🕵️ <b>Шпион</b> — видит ночные действия мафии\n"
            "💣 <b>Бомбист</b> — взрывается и убирает соседей при изгнании\n"
            "📰 <b>Журналист</b> — публикует роль одного игрока\n"
        ),
        "choose_language": "🌍 Выбери язык / Choose language:",
        "language_set": "✅ Язык установлен: Русский 🇷🇺",
        "feedback_ask": "📝 Напиши свой отзыв или предложение:",
        "feedback_sent": "✅ Отзыв отправлен! Спасибо.",
        "settings_title": "⚙️ <b>Настройки</b>",
        "admin_panel": "🛡️ <b>Панель администратора</b>",
        "admin_stats": "📊 Глобальная статистика",
        "admin_users": "👥 Пользователи",
        "admin_bans": "🚫 Баны",
        "admin_broadcast": "📢 Рассылка",
        "admin_feedback": "📝 Отзывы",
        "broadcast_ask": "📢 Введи текст рассылки:",
        "broadcast_sent": "✅ Рассылка отправлена {count} пользователям!",
        "global_stats_title": "📊 <b>Глобальная статистика</b>\n\n👥 Пользователей: <b>{users}</b>\n🎮 Игр сыграно: <b>{games}</b>\n🚫 Заблокировано: <b>{banned}</b>",
    },

    "en": {
        "welcome": "👋 Welcome to <b>HarshMafia Bot</b>!\n\nPlay Mafia right in Telegram!\n\nUse the menu below 👇",
        "menu_game": "🎮 Game",
        "menu_profile": "👤 Profile",
        "menu_stats": "📊 Stats",
        "menu_chats": "💬 Chats",
        "menu_top": "🏆 Top",
        "menu_help": "❓ Help",
        "menu_settings": "⚙️ Settings",
        "menu_language": "🌍 Language",
        "menu_admin": "🛡️ Admin Panel",
        "start_game": "🎮 Start Game",
        "join_game": "✅ Join",
        "leave_game": "❌ Leave",
        "game_started": "🎲 Game started! Registration open for {timeout} seconds.",
        "game_begin": "🚀 Game begins! Players: {count}",
        "role_assigned": "🎭 Your role: <b>{role}</b> {emoji}\n\n{description}",
        "night_begins": "🌙 <b>Night falls...</b>",
        "day_begins": "☀️ <b>Day begins!</b>",
        "discussion": "💬 Discussion! You have {time} seconds.",
        "vote_time": "🗳️ Vote! Who to eliminate?",
        "player_eliminated": "💀 {name} was eliminated! They were: <b>{role}</b>",
        "mafia_wins": "🔫 <b>Mafia wins!</b>",
        "citizens_win": "👥 <b>Citizens win!</b>",
        "not_enough_players": "❌ Not enough players! Minimum {min}.",
        "already_in_game": "⚠️ You're already in game!",
        "game_not_found": "❌ Game not found.",
        "profile_title": "👤 <b>{name}'s Profile</b>",
        "stats_games": "🎮 Games played: <b>{count}</b>",
        "stats_wins": "🏆 Wins: <b>{wins}</b>",
        "stats_losses": "💀 Losses: <b>{losses}</b>",
        "stats_kills": "🔪 Kills: <b>{kills}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        "stats_level": "📈 Level: <b>{level}</b>",
        "stats_winrate": "📊 Win rate: <b>{wr}%</b>",
        "top_players": "🏆 <b>Top Players</b>",
        "banned": "🚫 You are banned!\nReason: {reason}\nDate: {date}",
        "ban_success": "🚫 User {user} has been banned!\nReason: {reason}",
        "unban_success": "✅ User {user} has been unbanned!",
        "warn_success": "⚠️ User {user} received a warning ({count}/3)\nReason: {reason}",
        "warn_auto_ban": "🚫 User {user} auto-banned (3 warnings)!",
        "no_permission": "❌ You don't have permission!",
        "chats_title": "💬 <b>Our HarshMafia Chats</b>",
        "help_title": "❓ <b>Help</b>",
        "help_text": (
            "🎮 <b>Game commands:</b>\n"
            "/startgame — start a game\n"
            "/join — join game\n"
            "/leave — leave game\n"
            "/roles — list roles\n\n"
            "👤 <b>Profile:</b>\n"
            "/profile — your profile\n"
            "/stats — statistics\n"
            "/top — top players\n\n"
            "🛡️ <b>Moderation (admins only):</b>\n"
            "/ban — ban user\n"
            "/unban — unban user\n"
            "/warn — warn user\n"
            "/kick — kick user\n"
            "/mute — mute user\n\n"
            "⚙️ <b>Other:</b>\n"
            "/language — change language\n"
            "/feedback — send feedback\n"
            "/chats — our chats\n"
        ),
        "roles_list": (
            "🎭 <b>Game Roles:</b>\n\n"
            "👤 <b>Citizen</b> — votes and finds mafia\n"
            "🔫 <b>Mafia</b> — kills at night\n"
            "🎩 <b>Godfather</b> — mafia boss, hidden from detective\n"
            "🔍 <b>Detective</b> — checks player roles at night\n"
            "💊 <b>Doctor</b> — heals a player at night\n"
            "🛡️ <b>Bodyguard</b> — protects and kills attacker\n"
            "🔪 <b>Maniac</b> — kills alone, wins alone\n"
            "💃 <b>Prostitute</b> — blocks player action\n"
            "⭐ <b>Sheriff</b> — can shoot one player during day\n"
            "🕵️ <b>Spy</b> — sees mafia night actions\n"
            "💣 <b>Bomber</b> — kills neighbors when eliminated\n"
            "📰 <b>Journalist</b> — reveals one player's role\n"
        ),
        "choose_language": "🌍 Choose language / Выберите язык:",
        "language_set": "✅ Language set: English 🇬🇧",
        "feedback_ask": "📝 Write your feedback or suggestion:",
        "feedback_sent": "✅ Feedback sent! Thank you.",
        "settings_title": "⚙️ <b>Settings</b>",
        "admin_panel": "🛡️ <b>Admin Panel</b>",
        "admin_stats": "📊 Global Stats",
        "admin_users": "👥 Users",
        "admin_bans": "🚫 Bans",
        "admin_broadcast": "📢 Broadcast",
        "admin_feedback": "📝 Feedback",
        "broadcast_ask": "📢 Enter broadcast text:",
        "broadcast_sent": "✅ Broadcast sent to {count} users!",
        "global_stats_title": "📊 <b>Global Stats</b>\n\n👥 Users: <b>{users}</b>\n🎮 Games played: <b>{games}</b>\n🚫 Banned: <b>{banned}</b>",
    },

    "am": {
        "welcome": "👋 Բարի գալուստ <b>HarshMafia Bot</b>!\n\nԽաղա Մաֆիա Telegram-ում!\n\nՕգտագործիր ընտրացանկը 👇",
        "menu_game": "🎮 Խաղ",
        "menu_profile": "👤 Պրոֆիլ",
        "menu_stats": "📊 Վիճակագրություն",
        "menu_chats": "💬 Չաթեր",
        "menu_top": "🏆 Լավագույններ",
        "menu_help": "❓ Օգնություն",
        "menu_settings": "⚙️ Կարգավորումներ",
        "menu_language": "🌍 Լեզու",
        "menu_admin": "🛡️ Ադմin Panel",
        "start_game": "🎮 Սկսել խաղ",
        "join_game": "✅ Միանալ",
        "leave_game": "❌ Դուրս գալ",
        "game_started": "🎲 Խաղը սկսվեց! Գրանցումը բաց է {timeout} վայրկյան:",
        "game_begin": "🚀 Խաղը սկսվում է! Խաղացողներ: {count}",
        "role_assigned": "🎭 Քո դերը: <b>{role}</b> {emoji}\n\n{description}",
        "night_begins": "🌙 <b>Գիշերն է...</b>",
        "day_begins": "☀️ <b>Ցերեկ է!</b>",
        "discussion": "💬 Քննարկում! {time} վայրկյան:",
        "vote_time": "🗳️ Քվեարկություն! Ո՞ւմ հեռացնել:",
        "player_eliminated": "💀 {name}-ը հեռացվեց! Նա {role} էր:",
        "mafia_wins": "🔫 <b>Մաֆիան հաղթեց!</b>",
        "citizens_win": "👥 <b>Քաղաքացիները հաղթեցին!</b>",
        "not_enough_players": "❌ Բավարար խաղացողներ չկան! Մինիմում {min}:",
        "already_in_game": "⚠️ Դու արդեն խաղում ես!",
        "game_not_found": "❌ Խաղ չի գտնվել:",
        "profile_title": "👤 <b>{name}-ի պրոֆիլ</b>",
        "stats_games": "🎮 Խաղ: <b>{count}</b>",
        "stats_wins": "🏆 Հաղթանակ: <b>{wins}</b>",
        "stats_losses": "💀 Պարտություն: <b>{losses}</b>",
        "stats_kills": "🔪 Սպանություն: <b>{kills}</b>",
        "stats_xp": "⭐ XP: <b>{xp}</b>",
        "stats_level": "📈 Մակարդակ: <b>{level}</b>",
        "stats_winrate": "📊 Հաղթելու %: <b>{wr}%</b>",
        "top_players": "🏆 <b>Լավագույն խաղացողներ</b>",
        "banned": "🚫 Դու արգելափակված ես!\nՊատճառ: {reason}\nԱմսաթիվ: {date}",
        "ban_success": "🚫 {user}-ը արգելափակվեց!\nՊատճառ: {reason}",
        "unban_success": "✅ {user}-ը ապաարգելափակվեց!",
        "warn_success": "⚠️ {user}-ը ստացավ զգուշացում ({count}/3)\nՊատճառ: {reason}",
        "warn_auto_ban": "🚫 {user}-ը ավտոմատ արգելափակվեց (3 զգուշացում)!",
        "no_permission": "❌ Դու լիազորություն չունես!",
        "chats_title": "💬 <b>Մեր HarshMafia Չաթերը</b>",
        "help_title": "❓ <b>Օգնություն</b>",
        "help_text": "Օգտագործիր /startgame, /join, /leave, /profile, /stats, /top, /language",
        "roles_list": "🎭 Դերեր՝ Քաղաքացի, Մաֆիա, Դետեկտիվ, Բժիշկ, Մոլագար, Խաղաղ...",
        "choose_language": "🌍 Ընտրիր լեզու:",
        "language_set": "✅ Լեզուն կարգավորվեց: Հայերեն 🇦🇲",
        "feedback_ask": "📝 Գրիր կարծիքդ:",
        "feedback_sent": "✅ Կարծիքն ուղարկվեց! Շնորհակալություն:",
        "settings_title": "⚙️ <b>Կարգավորումներ</b>",
        "admin_panel": "🛡️ <b>Ադմin Վահանակ</b>",
        "admin_stats": "📊 Ընդհանուր վիճ.",
        "admin_users": "👥 Օգտատերեր",
        "admin_bans": "🚫 Արգելափակումներ",
        "admin_broadcast": "📢 Հաղորդագրություն",
        "admin_feedback": "📝 Կարծիքներ",
        "broadcast_ask": "📢 Գրիր հաղորդագրություն:",
        "broadcast_sent": "✅ Ուղարկվեց {count} օգտատերերի!",
        "global_stats_title": "📊 <b>Ընդհանուր վիճ.</b>\n\n👥 Օգտատեր: <b>{users}</b>\n🎮 Խաղ: <b>{games}</b>\n🚫 Արգ.: <b>{banned}</b>",
    },
}

# Fallback languages map for auto-detection
LANG_MAP = {
    "ru": "ru", "uk": "ru", "be": "ru", "kk": "ru",
    "en": "en", "de": "en", "fr": "en", "es": "en", "pt": "en",
    "it": "en", "nl": "en", "pl": "en", "cs": "en",
    "hy": "am",
}

def t(key: str, lang: str = "en", **kwargs) -> str:
    """Get translation for key in given language."""
    lang_data = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_data.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass
    return text

def get_user_lang(user) -> str:
    """Get user language from DB user dict."""
    if isinstance(user, dict):
        lang = user.get("lang", "ru")
        return lang if lang in TRANSLATIONS else "ru"
    return "ru"
