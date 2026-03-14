from aiogram import Bot
from aiogram import Dispatcher
from aiogram.utils import executor

from config import BOT_TOKEN

from database.db import connect
from database.models import create_tables
from handlers import join
from handlers import start
from handlers import invite
from handlers import profile
from handlers import leaderboard
from handlers import rating


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def on_startup(dp):

    await connect()

    await create_tables()

    start.register(dp)
    invite.register(dp)
    profile.register(dp)
    leaderboard.register(dp)
    rating.register(dp)


if __name__ == "__main__":

    executor.start_polling(
        dp,
        on_startup=on_startup
    )
