from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.db import pool


async def profile_cmd(message: types.Message):

    user_id = message.from_user.id

    async with pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id=$1",
            user_id
        )

    if not user:

        return await message.answer("Profile not found")

    text = f"""
👤 Profile

Invites: {user['invites']}

Good: {user['good']}
Bad: {user['bad']}

Verified: {user['verified']}
"""

    await message.answer(text)


def register(dp: Dispatcher):

    dp.register_message_handler(
        profile_cmd,
        commands=["profile"]
    )
