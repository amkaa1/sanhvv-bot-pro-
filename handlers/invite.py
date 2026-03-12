from aiogram import types

def register(dp):

    @dp.message_handler(commands=["invite"])
    async def invite(message: types.Message):

        user_id = message.from_user.id

        link = f"https://t.me/sanhvvmgl2026_bot?start={user_id}"

        await message.reply(
f"""
Invite friends

Your link:

{link}
"""
)
