from aiogram import types
import database
import time

cooldowns = {}

def register(dp):

    @dp.message_handler(commands=["rate"])
    async def rate(message: types.Message):

        args = message.text.split()

        if len(args) != 3:
            return

        username = args[1]
        rating = args[2]

        voter = message.from_user.id

        now = time.time()

        if voter not in cooldowns:
            cooldowns[voter] = []

        votes = [v for v in cooldowns[voter] if now - v < 86400]

        if len(votes) >= 2:
            await message.answer("Vote cooldown active")
            return

        votes.append(now)
        cooldowns[voter] = votes
