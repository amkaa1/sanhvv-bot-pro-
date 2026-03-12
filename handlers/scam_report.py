from aiogram import types
from database import cursor, conn
from config import SCAM_REPORT_LIMIT

def register(dp):

    @dp.message_handler(commands=['report'])
    async def report(message: types.Message):

        args = message.text.split()

        if len(args) != 2:
            return

        target = int(args[1])

        cursor.execute("INSERT INTO scam_reports VALUES(?,?)",
                       (message.from_user.id, target))

        cursor.execute("SELECT COUNT(*) FROM scam_reports WHERE target=?", (target,))
        count = cursor.fetchone()[0]

        if count >= SCAM_REPORT_LIMIT:

            cursor.execute("INSERT OR IGNORE INTO blacklist VALUES(?)", (target,))
            conn.commit()

            await message.reply("User added to scam blacklist")

        else:
            conn.commit()
            await message.reply("Report submitted")
