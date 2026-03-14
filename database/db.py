import asyncpg
from config import DATABASE_URL

pool = None

async def connect():

    global pool

    pool = await asyncpg.create_pool(
        DATABASE_URL
    )


async def get_conn():

    return pool.acquire()
