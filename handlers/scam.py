from aiogram import types
import database

def register(dp):

    @dp.message_handler(commands=["report"])
    async def report(message: types.Message):

        args = message.text.split()

        if len(args) < 3:
            return

        target = args[1]
        reason = " ".join(args[2:])
