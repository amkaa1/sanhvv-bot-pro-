from aiogram import types
from database import cursor

def register(dp):

    @dp.message_handler(commands=['topinvite'])
    async def leaderboard(message: types.Message):

        cursor.execute("SELECT user_id, invites FROM users ORDER BY invites DESC LIMIT 10")

        users = cursor.fetchall()

        text = "Top Inviters\n\n"

        for i, u in enumerate(users, start=1):

            text += f"{i}. {u[0]} — {u[1]} invites\n"

        await message.reply(text)
