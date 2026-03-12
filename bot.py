from aiogram import Bot, Dispatcher, executor, types
import config
import database

from handlers import start
from handlers import profile
from handlers import rating
from handlers import invite
from handlers import reward
from handlers import scam
from handlers import admin

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)


start.register(dp)
profile.register(dp)
rating.register(dp)
invite.register(dp)
reward.register(dp)
scam.register(dp)
admin.register(dp)


async def on_startup(dp):

    await database.connect()
    await database.create_tables()


if __name__ == "__main__":

    executor.start_polling(dp, on_startup=on_startup)
