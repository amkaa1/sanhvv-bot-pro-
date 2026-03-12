from aiogram import types
from database import cursor, conn
from config import GOOD_TO_VERIFY

def register(dp):

    @dp.message_handler(commands=['rate'])
    async def rate(message: types.Message):

        args = message.text.split()

        if len(args) != 3:
            return

        target = int(args[1])
        vote = args[2]

        if vote == "good":
            cursor.execute("UPDATE users SET good = good + 1 WHERE user_id=?", (target,))
        else:
            cursor.execute("UPDATE users SET bad = bad + 1 WHERE user_id=?", (target,))

        cursor.execute("SELECT good FROM users WHERE user_id=?", (target,))
        good = cursor.fetchone()[0]

        if good >= GOOD_TO_VERIFY:
            cursor.execute("UPDATE users SET verified = 1 WHERE user_id=?", (target,))

        conn.commit()

        await message.reply("Vote added")
