import asyncpg
import os

pool = None

async def connect():
    global pool
    pool = await asyncpg.create_pool(os.getenv("DATABASE_URL"))
async def create_tables():

    async with pool.acquire() as conn:

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS users(
            telegram_id BIGINT PRIMARY KEY,
            username TEXT,
            invites INT DEFAULT 0,
            good INT DEFAULT 0,
            bad INT DEFAULT 0,
            verified BOOLEAN DEFAULT FALSE,
            scam_reports INT DEFAULT 0,
            muted BOOLEAN DEFAULT FALSE,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS invites(
            inviter BIGINT,
            invited BIGINT UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS ratings(
            voter BIGINT,
            target BIGINT,
            rating TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS scam_reports(
            reporter BIGINT,
            target BIGINT,
            reason TEXT
        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS rewards(
            user_id BIGINT,
            reward_level INT,
            claimed BOOLEAN DEFAULT FALSE
        )

        """)
