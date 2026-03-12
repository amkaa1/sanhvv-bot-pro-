from aiogram import types

def register(dp):

    @dp.message_handler(commands=['invite'])
    async def invite(message: types.Message):

        user_id = message.from_user.id

        link = f"https://t.me/YOUR_BOT?start={user_id}"

        text = f"""
Invite friends and earn rewards

Your link:
{link}
"""

        await message.reply(text)
