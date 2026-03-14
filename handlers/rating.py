from aiogram import types
from aiogram.dispatcher import Dispatcher
from database.db import pool


async def rate(message: types.Message):

    args = message.text.split()

    if len(args) != 3:

        return await message.answer(
            "/rate user_id good|bad"
        )

    target = int(args[1])
    rate_type = args[2]

    voter = message.from_user.id

    async with pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO ratings(
            voter,
            target,
            type
            )
            VALUES($1,$2,$3)
            """,
            voter,
            target,
            rate_type
        )

        if rate_type == "good":

            await conn.execute(
                "UPDATE users SET good=good+1 WHERE user_id=$1",
                target
            )

        else:

            await conn.execute(
                "UPDATE users SET bad=bad+1 WHERE user_id=$1",
                target
            )

    await message.answer("Vote recorded")


def register(dp: Dispatcher):

    dp.register_message_handler(
        rate,
        commands=["rate"]
    )
