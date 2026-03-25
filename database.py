import sqlite3
import json
from config import DB_PATH
from datetime import datetime

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        lang TEXT DEFAULT 'ru',
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        games_played INTEGER DEFAULT 0,
        games_won INTEGER DEFAULT 0,
        games_lost INTEGER DEFAULT 0,
        kills INTEGER DEFAULT 0,
        deaths INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        ban_reason TEXT DEFAULT NULL,
        banned_by INTEGER DEFAULT NULL,
        ban_date TEXT DEFAULT NULL,
        warn_count INTEGER DEFAULT 0,
        is_admin INTEGER DEFAULT 0,
        coins INTEGER DEFAULT 0,
        joined_date TEXT DEFAULT NULL,
        last_seen TEXT DEFAULT NULL,
        favorite_role TEXT DEFAULT NULL,
        bio TEXT DEFAULT NULL,
        achievements TEXT DEFAULT '[]'
    )
    """)

    # Games table
    c.execute("""
    CREATE TABLE IF NOT EXISTS games (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id INTEGER,
        started_by INTEGER,
        start_time TEXT,
        end_time TEXT,
        winner TEXT,
        players TEXT,
        roles TEXT,
        rounds INTEGER DEFAULT 0,
        status TEXT DEFAULT 'waiting'
    )
    """)

    # Game players table
    c.execute("""
    CREATE TABLE IF NOT EXISTS game_players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_id INTEGER,
        user_id INTEGER,
        role TEXT,
        is_alive INTEGER DEFAULT 1,
        kills INTEGER DEFAULT 0,
        xp_earned INTEGER DEFAULT 0,
        won INTEGER DEFAULT 0
    )
    """)

    # Warns table
    c.execute("""
    CREATE TABLE IF NOT EXISTS warns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        chat_id INTEGER,
        reason TEXT,
        warned_by INTEGER,
        date TEXT
    )
    """)

    # Ban history
    c.execute("""
    CREATE TABLE IF NOT EXISTS ban_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        reason TEXT,
        by_admin INTEGER,
        date TEXT
    )
    """)

    # Chats table
    c.execute("""
    CREATE TABLE IF NOT EXISTS registered_chats (
        chat_id INTEGER PRIMARY KEY,
        chat_name TEXT,
        chat_link TEXT,
        lang TEXT DEFAULT 'ru',
        added_by INTEGER,
        added_date TEXT,
        games_count INTEGER DEFAULT 0
    )
    """)

    # Achievements table
    c.execute("""
    CREATE TABLE IF NOT EXISTS achievements (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        achievement TEXT,
        date TEXT
    )
    """)

    # Feedback table
    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        date TEXT,
        status TEXT DEFAULT 'new'
    )
    """)

    conn.commit()
    conn.close()

# ─── USER FUNCTIONS ────────────────────────────────────────────────────

def get_or_create_user(user_id, username=None, first_name=None):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()
    if not user:
        now = datetime.now().isoformat()
        c.execute("""INSERT INTO users 
            (user_id, username, first_name, joined_date, last_seen)
            VALUES (?,?,?,?,?)""",
            (user_id, username, first_name, now, now))
        conn.commit()
        c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
        user = c.fetchone()
    conn.close()
    return dict(user)

def update_user_lang(user_id, lang):
    conn = get_connection()
    conn.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, user_id))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def update_user_xp(user_id, xp_add):
    user = get_user(user_id)
    if not user:
        return
    new_xp = user['xp'] + xp_add
    new_level = 1 + new_xp // 200
    conn = get_connection()
    conn.execute("UPDATE users SET xp=?, level=? WHERE user_id=?", (new_xp, new_level, user_id))
    conn.commit()
    conn.close()

def update_last_seen(user_id):
    conn = get_connection()
    conn.execute("UPDATE users SET last_seen=? WHERE user_id=?",
                 (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()

# ─── BAN FUNCTIONS ────────────────────────────────────────────────────

def ban_user(user_id, reason, by_admin):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("""UPDATE users SET is_banned=1, ban_reason=?, banned_by=?, ban_date=?
                    WHERE user_id=?""", (reason, by_admin, now, user_id))
    conn.execute("""INSERT INTO ban_history (user_id, action, reason, by_admin, date)
                    VALUES (?,?,?,?,?)""", (user_id, 'ban', reason, by_admin, now))
    conn.commit()
    conn.close()

def unban_user(user_id, by_admin):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("""UPDATE users SET is_banned=0, ban_reason=NULL, banned_by=NULL, ban_date=NULL
                    WHERE user_id=?""", (user_id,))
    conn.execute("""INSERT INTO ban_history (user_id, action, reason, by_admin, date)
                    VALUES (?,?,?,?,?)""", (user_id, 'unban', '', by_admin, now))
    conn.commit()
    conn.close()

def is_banned(user_id):
    user = get_user(user_id)
    return user and user['is_banned'] == 1

def get_ban_info(user_id):
    user = get_user(user_id)
    if user and user['is_banned']:
        return {"reason": user['ban_reason'], "by": user['banned_by'], "date": user['ban_date']}
    return None

# ─── WARN FUNCTIONS ───────────────────────────────────────────────────

def warn_user(user_id, chat_id, reason, by_admin):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("""INSERT INTO warns (user_id, chat_id, reason, warned_by, date)
                    VALUES (?,?,?,?,?)""", (user_id, chat_id, reason, by_admin, now))
    conn.execute("UPDATE users SET warn_count = warn_count + 1 WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    user = get_user(user_id)
    return user['warn_count'] + 1

def get_warns(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM warns WHERE user_id=? ORDER BY date DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def reset_warns(user_id):
    conn = get_connection()
    conn.execute("UPDATE users SET warn_count=0 WHERE user_id=?", (user_id,))
    conn.execute("DELETE FROM warns WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()

# ─── ADMIN FUNCTIONS ──────────────────────────────────────────────────

def set_admin(user_id, is_admin=True):
    conn = get_connection()
    conn.execute("UPDATE users SET is_admin=? WHERE user_id=?", (1 if is_admin else 0, user_id))
    conn.commit()
    conn.close()

def is_admin_db(user_id):
    user = get_user(user_id)
    return user and (user['is_admin'] == 1)

# ─── STATS FUNCTIONS ──────────────────────────────────────────────────

def get_top_players(limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT user_id, username, first_name, xp, level, games_won, games_played, kills
                 FROM users WHERE is_banned=0
                 ORDER BY xp DESC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_top_killers(limit=10):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""SELECT user_id, username, first_name, kills, xp
                 FROM users WHERE is_banned=0
                 ORDER BY kills DESC LIMIT ?""", (limit,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_game_stats(user_id, won, kills=0):
    conn = get_connection()
    if won:
        conn.execute("""UPDATE users SET games_played=games_played+1, 
                        games_won=games_won+1, kills=kills+? WHERE user_id=?""",
                     (kills, user_id))
    else:
        conn.execute("""UPDATE users SET games_played=games_played+1,
                        games_lost=games_lost+1, kills=kills+? WHERE user_id=?""",
                     (kills, user_id))
    conn.commit()
    conn.close()

# ─── ACHIEVEMENTS ─────────────────────────────────────────────────────

ACHIEVEMENTS_LIST = {
    "first_game": {"emoji": "🎮", "name": "First Game", "desc": "Play your first game"},
    "first_win": {"emoji": "🏆", "name": "First Win", "desc": "Win your first game"},
    "serial_killer": {"emoji": "🔪", "name": "Serial Killer", "desc": "Kill 10 players"},
    "detective_pro": {"emoji": "🔍", "name": "Detective Pro", "desc": "Correctly identify 5 mafia"},
    "survivor": {"emoji": "🛡️", "name": "Survivor", "desc": "Survive 10 games"},
    "veteran": {"emoji": "⭐", "name": "Veteran", "desc": "Play 50 games"},
    "legend": {"emoji": "👑", "name": "Legend", "desc": "Win 25 games"},
    "godfather": {"emoji": "🎩", "name": "Godfather", "desc": "Win as mafia 10 times"},
}

def give_achievement(user_id, achievement_key):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM achievements WHERE user_id=? AND achievement=?",
              (user_id, achievement_key))
    if not c.fetchone():
        now = datetime.now().isoformat()
        conn.execute("INSERT INTO achievements (user_id, achievement, date) VALUES (?,?,?)",
                     (user_id, achievement_key, now))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_user_achievements(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT achievement, date FROM achievements WHERE user_id=?", (user_id,))
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ─── FEEDBACK ─────────────────────────────────────────────────────────

def save_feedback(user_id, message):
    conn = get_connection()
    now = datetime.now().isoformat()
    conn.execute("INSERT INTO feedback (user_id, message, date) VALUES (?,?,?)",
                 (user_id, message, now))
    conn.commit()
    conn.close()

def get_all_feedback():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM feedback ORDER BY date DESC")
    rows = c.fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ─── GLOBAL STATS ─────────────────────────────────────────────────────

def get_global_stats():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) as total_users FROM users")
    total_users = c.fetchone()['total_users']
    c.execute("SELECT COUNT(*) as total_games FROM games WHERE status='finished'")
    total_games = c.fetchone()['total_games']
    c.execute("SELECT COUNT(*) as banned FROM users WHERE is_banned=1")
    banned = c.fetchone()['banned']
    conn.close()
    return {"total_users": total_users, "total_games": total_games, "banned": banned}
