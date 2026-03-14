from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.db import pool


async def user_join(message: types.Message):

    for user in message.new_chat_members:

        user_id = user.id

        async with pool.acquire() as conn:

            data = await conn.fetchrow(
                "SELECT invited_by FROM users WHERE user_id=$1",
                user_id
            )

            if not data:
                return

            inviter = data["invited_by"]

            if not inviter:
                return

            await conn.execute(
                """
                INSERT INTO invites(inviter,invited)
                VALUES($1,$2)
                """,
                inviter,
                user_id
            )

            await conn.execute(
                """
                UPDATE users
                SET invites = invites + 1
                WHERE user_id=$1
                """,
                inviter
            )


def register(dp: Dispatcher):

    dp.register_message_handler(
        user_join,
        content_types=types.ContentType.NEW_CHAT_MEMBERS
    )
