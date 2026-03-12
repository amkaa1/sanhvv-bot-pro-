from aiogram import types
import database

def register(dp):

    @dp.message_handler(commands=["topinvite"])
    async def topinvite(message: types.Message):

        async with database.pool.acquire() as conn:

            rows = await conn.fetch("""

            SELECT username,invites
            FROM users
            ORDER BY invites DESC
            LIMIT 10

            """)

        text = "🏆 Invite Leaderboard\n\n"

        i = 1

        for r in rows:

            text += f"{i}. @{r['username']} — {r['invites']}\n"
            i += 1

        await message.answer(text)
