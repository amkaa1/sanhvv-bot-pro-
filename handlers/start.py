from aiogram import types
import database

def register(dp):

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):

        args = message.get_args()

        async with database.pool.acquire() as conn:

            await conn.execute("""

            INSERT INTO users(telegram_id,username)
            VALUES($1,$2)
            ON CONFLICT DO NOTHING

            """,
            message.from_user.id,
            message.from_user.username
            )


        if args:

            inviter = int(args)

            async with database.pool.acquire() as conn:

                exists = await conn.fetchrow("""

                SELECT * FROM invites
                WHERE invited=$1

                """, message.from_user.id)

                if not exists:

                    await conn.execute("""

                    INSERT INTO invites(inviter,invited)
                    VALUES($1,$2)

                    """, inviter, message.from_user.id)

                    await conn.execute("""

                    UPDATE users
                    SET invites = invites + 1
                    WHERE telegram_id=$1

                    """, inviter)


        await message.answer(
            "Welcome to SanhvvMGL2026 Bot\n\n"
            "/profile\n"
            "/topinvite\n"
        )
