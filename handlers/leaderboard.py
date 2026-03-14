from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.db import pool


async def leaderboard(message: types.Message):

    async with pool.acquire() as conn:

        rows = await conn.fetch(
            "SELECT * FROM users ORDER BY invites DESC LIMIT 10"
        )

    text = "🏆 TOP INVITERS\n\n"

    rank = 1

    for r in rows:

        text += f"{rank}. {r['username']} — {r['invites']}\n"

        rank += 1

    await message.answer(text)


def register(dp: Dispatcher):

    dp.register_message_handler(
        leaderboard,
        commands=["topinvite"]
    )
