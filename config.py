import os

# ===================== BOT CONFIG =====================
BOT_TOKEN = os.getenv("BOT_TOKEN", "8204466219:AAFmb3IS1523JYJp6KH55Zi4sGJxs5UtVnQ")

# ===================== OWNER / ADMINS =====================
OWNER_ID = 7950038145  # HarshMafia Owner

ADMIN_IDS = [
    7950038145,  # Owner
    # Add more admin IDs here
]

# ===================== CHATS =====================
CHATS = {
    "main": {
        "name": "HarshMafia - Main",
        "link": "https://t.me/harshmafia",
        "emoji": "🌍",
        "lang": "multi"
    },
    "russian": {
        "name": "HarshMafia - Russian",
        "link": "https://t.me/harshmafiaru",
        "emoji": "🇷🇺",
        "lang": "ru"
    },
    "armenian": {
        "name": "HarshMafia - Armenian",
        "link": "https://t.me/harshmafiaarm",
        "emoji": "🇦🇲",
        "lang": "am"
    },
    "english": {
        "name": "HarshMafia - English",
        "link": "https://t.me/harshmafiaen",
        "emoji": "🇬🇧",
        "lang": "en"
    },
}

# ===================== GAME SETTINGS =====================
MIN_PLAYERS = 4
MAX_PLAYERS = 20
GAME_JOIN_TIMEOUT = 120       # seconds to join
DISCUSSION_TIME = 90          # seconds for discussion
VOTE_TIME = 60                # seconds for voting
NIGHT_TIME = 30               # seconds for night actions

# Roles distribution (players -> roles count)
ROLES_DISTRIBUTION = {
    4:  {"mafia": 1, "detective": 0, "doctor": 0, "citizen": 3},
    5:  {"mafia": 1, "detective": 1, "doctor": 0, "citizen": 3},
    6:  {"mafia": 1, "detective": 1, "doctor": 1, "citizen": 3},
    7:  {"mafia": 2, "detective": 1, "doctor": 1, "citizen": 3},
    8:  {"mafia": 2, "detective": 1, "doctor": 1, "citizen": 4},
    9:  {"mafia": 2, "detective": 1, "doctor": 1, "citizen": 5},
    10: {"mafia": 3, "detective": 1, "doctor": 1, "citizen": 5},
    12: {"mafia": 3, "detective": 2, "doctor": 1, "citizen": 6},
    15: {"mafia": 4, "detective": 2, "doctor": 1, "citizen": 8},
    20: {"mafia": 5, "detective": 2, "doctor": 2, "citizen": 11},
}

# ===================== ROLES =====================
ALL_ROLES = [
    "citizen", "mafia", "detective", "doctor",
    "maniac", "godfather", "prostitute", "bodyguard",
    "sheriff", "spy", "bomber", "journalist"
]

ROLE_EMOJIS = {
    "citizen": "👤",
    "mafia": "🔫",
    "detective": "🔍",
    "doctor": "💊",
    "maniac": "🔪",
    "godfather": "🎩",
    "prostitute": "💃",
    "bodyguard": "🛡️",
    "sheriff": "⭐",
    "spy": "🕵️",
    "bomber": "💣",
    "journalist": "📰",
}

# ===================== XP / RATING =====================
XP_WIN = 50
XP_LOSE = 10
XP_KILL = 20
XP_SURVIVE_ROUND = 5
XP_CORRECT_VOTE = 15

# ===================== DATABASE =====================
DB_PATH = "harshmafia.db"
