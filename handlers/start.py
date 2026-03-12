from aiogram import types
from database import cursor, conn

def register(dp):

    @dp.message_handler(commands=['start'])
    async def start(message: types.Message):

        ref = message.get_args()
        user_id = message.from_user.id

        cursor.execute("SELECT user_id FROM users WHERE user_id=?", (user_id,))
        user = cursor.fetchone()

        if not user:

            invited_by = None

            if ref and ref.isdigit():
                invited_by = int(ref)

                if invited_by != user_id:
                    cursor.execute("UPDATE users SET invites = invites + 1 WHERE user_id=?", (invited_by,))

            cursor.execute(
                "INSERT INTO users(user_id, invited_by) VALUES(?,?)",
                (user_id, invited_by)
            )

            conn.commit()

        await message.reply("Welcome to the group bot.")
