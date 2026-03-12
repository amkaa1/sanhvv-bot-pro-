from aiogram import types
import database

def register(dp):

    @dp.message_handler(commands=["profile"])
    async def profile(message: types.Message):

        async with database.pool.acquire() as conn:

            user = await conn.fetchrow("""

            SELECT * FROM users
            WHERE telegram_id=$1

            """, message.from_user.id)

        if not user:

            await message.answer("User not found")
            return

        verified = "✅" if user["verified"] else "❌"

        text = f"""
👤 Profile

👍 Good: {user['good']}
👎 Bad: {user['bad']}

📨 Invites: {user['invites']}

✔ Verified: {verified}

⚠ Scam reports: {user['scam_reports']}
"""

        await message.answer(text)
