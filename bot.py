from aiogram import Bot, Dispatcher, executor
from config import BOT_TOKEN

from handlers import start, invite, profile, rating, leaderboard, scam_report, admin

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

start.register(dp)
invite.register(dp)
profile.register(dp)
rating.register(dp)
leaderboard.register(dp)
scam_report.register(dp)
admin.register(dp)

if __name__ == "__main__":
    executor.start_polling(dp)
