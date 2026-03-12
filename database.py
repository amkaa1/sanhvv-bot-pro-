import sqlite3

conn = sqlite3.connect("bot.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
user_id INTEGER PRIMARY KEY,
invited_by INTEGER,
invites INTEGER DEFAULT 0,
good INTEGER DEFAULT 0,
bad INTEGER DEFAULT 0,
verified INTEGER DEFAULT 0
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS votes(
voter INTEGER,
target INTEGER,
date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS scam_reports(
reporter INTEGER,
target INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blacklist(
user_id INTEGER PRIMARY KEY
)
""")

conn.commit()
