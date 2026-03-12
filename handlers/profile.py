from aiogram import types
from database import cursor

def register(dp):

    @dp.message_handler(commands=['profile'])
    async def profile(message: types.Message):

        user_id = message.from_user.id

        cursor.execute("SELECT invites,good,bad,verified FROM users WHERE user_id=?", (user_id,))
        data = cursor.fetchone()

        invites, good, bad, verified = data

        badge = "✅ Verified" if verified else "❌ Not verified"

        text = f"""
ID: {user_id}

Invites: {invites}

Good: {good}
Bad: {bad}

Status: {badge}
"""

        await message.reply(text)
