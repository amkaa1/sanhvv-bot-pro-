from aiogram import Bot, Dispatcher, executor, types
from config import BOT_TOKEN, GROUP_ID
import database
from keyboards import main_menu

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# START COMMAND

@dp.message_handler(commands=['start'])
async def start(message: types.Message):

    args = message.get_args()

    user_id = message.from_user.id
    username = message.from_user.username

    async with database.pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id=$1",
            user_id
        )

        if not user:

            invited_by = None

            if args:
                invited_by = int(args)

            await conn.execute(
                """
                INSERT INTO users(user_id,username,invited_by)
                VALUES($1,$2,$3)
                """,
                user_id,
                username,
                invited_by
            )

    await message.answer(
        "Welcome to the invite system",
        reply_markup=main_menu()
    )


# INVITE LINK

@dp.message_handler(commands=['invite'])
async def invite(message: types.Message):

    user_id = message.from_user.id

    link = f"https://t.me/sanhvv2026mgl?start={user_id}"

    text = f"""
📨 Your invite link

{link}

Invite friends and earn rewards
"""

    await message.answer(text)


# PROFILE

@dp.message_handler(commands=['profile'])
async def profile(message: types.Message):

    user_id = message.from_user.id

    async with database.pool.acquire() as conn:

        user = await conn.fetchrow(
            "SELECT * FROM users WHERE user_id=$1",
            user_id
        )

    if not user:
        return await message.answer("User not found")

    text = f"""
👤 Profile

Invites: {user['invites']}
Good: {user['good']}
Bad: {user['bad']}

Verified: {user['verified']}
"""

    await message.answer(text)


# LEADERBOARD

@dp.message_handler(commands=['topinvite'])
async def leaderboard(message: types.Message):

    async with database.pool.acquire() as conn:

        rows = await conn.fetch(
            "SELECT * FROM users ORDER BY invites DESC LIMIT 10"
        )

    text = "🏆 TOP INVITERS\n\n"

    rank = 1

    for r in rows:

        text += f"{rank}. {r['username']} — {r['invites']}\n"

        rank += 1

    await message.answer(text)


# RATE SYSTEM

@dp.message_handler(commands=['rate'])
async def rate(message: types.Message):

    args = message.text.split()

    if len(args) != 3:
        return await message.answer(
            "/rate user_id good|bad"
        )

    target = int(args[1])
    rate_type = args[2]

    voter = message.from_user.id

    async with database.pool.acquire() as conn:

        await conn.execute(
            """
            INSERT INTO ratings(voter,target,type)
            VALUES($1,$2,$3)
            """,
            voter,
            target,
            rate_type
        )

        if rate_type == "good":

            await conn.execute(
                """
                UPDATE users
                SET good = good + 1
                WHERE user_id=$1
                """,
                target
            )

        else:

            await conn.execute(
                """
                UPDATE users
                SET bad = bad + 1
                WHERE user_id=$1
                """,
                target
            )

    await message.answer("Vote recorded")


# GROUP JOIN EVENT

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):

    for user in message.new_chat_members:

        user_id = user.id

        async with database.pool.acquire() as conn:

            record = await conn.fetchrow(
                "SELECT invited_by FROM users WHERE user_id=$1",
                user_id
            )

            if record and record["invited_by"]:

                inviter = record["invited_by"]

                await conn.execute(
                    """
                    UPDATE users
                    SET invites = invites + 1
                    WHERE user_id=$1
                    """,
                    inviter
                )


# START BOT

async def on_startup(dp):

    await database.connect()
    await database.create_tables()

if __name__ == "__main__":

    executor.start_polling(
        dp,
        on_startup=on_startup
    )
