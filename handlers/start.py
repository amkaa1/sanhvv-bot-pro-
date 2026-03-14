from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.db import pool


async def start_cmd(message: types.Message):

    args = message.get_args()

    user_id = message.from_user.id
    username = message.from_user.username

    invited_by = None

    if args:

        invited_by = int(args)

    async with pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id=$1",
            user_id
        )

        if not user:

            await conn.execute(
                """
                INSERT INTO users(user_id,username,invited_by)
                VALUES($1,$2,$3)
                """,
                user_id,
                username,
                invited_by
            )

    await message.answer("Welcome 👋")


def register(dp: Dispatcher):

    dp.register_message_handler(
        start_cmd,
        commands=["start"]
    )
