from .db import pool

async def create_tables():

    async with pool.acquire() as conn:

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS users(

        user_id BIGINT PRIMARY KEY,
        username TEXT,
        invited_by BIGINT,
        invites INT DEFAULT 0,
        good INT DEFAULT 0,
        bad INT DEFAULT 0,
        verified BOOLEAN DEFAULT FALSE

        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS ratings(

        voter BIGINT,
        target BIGINT,
        type TEXT,
        time TIMESTAMP DEFAULT NOW()

        )

        """)

        await conn.execute("""

        CREATE TABLE IF NOT EXISTS invites(

        inviter BIGINT,
        invited BIGINT,
        time TIMESTAMP DEFAULT NOW()

        )

        """)
