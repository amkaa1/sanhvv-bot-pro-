from aiogram import types
from database import cursor, conn
from datetime import datetime

def register(dp):

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message):

        user_id = message.from_user.id
        ref = message.get_args()

        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        exists = cursor.fetchone()

        if not exists:

            invited_by = None

            if ref.isdigit():

                invited_by = int(ref)

                if invited_by != user_id:
                    cursor.execute(
                        "UPDATE users SET invites = invites + 1 WHERE user_id=?",
                        (invited_by,)
                    )

            cursor.execute(
                "INSERT INTO users VALUES(?,?,?,?,?,?,?)",
                (user_id, invited_by, 0, 0, 0, 0, datetime.now())
            )

            conn.commit()

        await message.answer("Bot activated.")
