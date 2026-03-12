from aiogram import types
import database
import config

def register(dp):

    @dp.message_handler(commands=["verify"])
    async def verify(message: types.Message):

        if message.from_user.username != config.ADMIN_USERNAME:
            return
