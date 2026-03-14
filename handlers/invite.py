from aiogram import types
from aiogram.dispatcher import Dispatcher


async def invite_cmd(message: types.Message):

    user_id = message.from_user.id

    link = f"https://t.me/sanhvv2026mgl?start={user_id}"

    text = f"""
📨 Your Invite Link

{link}

Invite users to earn rewards
"""

    await message.answer(text)


def register(dp: Dispatcher):

    dp.register_message_handler(
        invite_cmd,
        commands=["invite"]
    )
