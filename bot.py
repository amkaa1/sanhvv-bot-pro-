import os
import time
import asyncpg
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

BOT_USERNAME = "sanhvvmgl2026_bot"
ADMIN_ID = 847622607
GROUP_ID = -1003744595373

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

pool = None
vote_cooldowns = {}

REWARDS = {
100:"20k",
500:"100k",
1000:"300k",
2000:"600k"
}

async def connect_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users(
        telegram_id BIGINT PRIMARY KEY,
        username TEXT,
        invites INT DEFAULT 0,
        good INT DEFAULT 0,
        bad INT DEFAULT 0,
        verified BOOLEAN DEFAULT FALSE,
        scam_reports INT DEFAULT 0
        )
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS invites(
        inviter BIGINT,
        invited BIGINT UNIQUE
        )
        """)

        await conn.execute("""
        CREATE TABLE IF NOT EXISTS blacklist(
        telegram_id BIGINT PRIMARY KEY
        )
        """)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username

    async with pool.acquire() as conn:

        await conn.execute("""
        INSERT INTO users(telegram_id,username)
        VALUES($1,$2)
        ON CONFLICT DO NOTHING
        """,user_id,username)

    if args:

        inviter=int(args)

        if inviter==user_id:
            return

        if message.from_user.is_bot:
            return

        try:
            member=await bot.get_chat_member(GROUP_ID,user_id)

            if member.status not in ["member","administrator","creator"]:
                await message.answer("Group join хийгээд start дарна уу")
                return
        except:
            return

        async with pool.acquire() as conn:

            exist=await conn.fetchrow("""
            SELECT * FROM invites
            WHERE invited=$1
            """,user_id)

            if not exist:

                await conn.execute("""
                INSERT INTO invites(inviter,invited)
                VALUES($1,$2)
                """,inviter,user_id)

                await conn.execute("""
                UPDATE users
                SET invites=invites+1
                WHERE telegram_id=$1
                """,inviter)

                data=await conn.fetchrow("""
                SELECT invites FROM users
                WHERE telegram_id=$1
                """,inviter)

                if data["invites"] in REWARDS:

                    await bot.send_message(
                        inviter,
                        f"🎉 Reward reached\n{data['invites']} invites\nReward {REWARDS[data['invites']]}"
                    )

@dp.message_handler(commands=["invite"])
async def invite(message:types.Message):

    link=f"https://t.me/{BOT_USERNAME}?start={message.from_user.id}"

    await message.answer(f"🔗 Invite link\n{link}")

@dp.message_handler(commands=["profile"])
async def profile(message:types.Message):

    async with pool.acquire() as conn:

        user=await conn.fetchrow("""
        SELECT * FROM users
        WHERE telegram_id=$1
        """,message.from_user.id)

    verified="✅" if user["verified"] else "❌"

    await message.answer(f"""
Profile

Invites: {user['invites']}

Good: {user['good']}
Bad: {user['bad']}

Verified: {verified}
Scam reports: {user['scam_reports']}
""")

@dp.message_handler(commands=["topinvite"])
async def leaderboard(message:types.Message):

    async with pool.acquire() as conn:

        rows=await conn.fetch("""
        SELECT username,invites
        FROM users
        ORDER BY invites DESC
        LIMIT 10
        """)

    text="🏆 Leaderboard\n\n"

    i=1

    for r in rows:

        text+=f"{i}. @{r['username']} — {r['invites']}\n"
        i+=1

    await message.answer(text)

@dp.message_handler(commands=["rate"])
async def rate(message:types.Message):

    args=message.text.split()

    if len(args)!=3:
        return

    target=int(args[1])
    rating=args[2]

    voter=message.from_user.id
    now=time.time()

    if voter not in vote_cooldowns:
        vote_cooldowns[voter]=[]

    votes=[v for v in vote_cooldowns[voter] if now-v<86400]

    if len(votes)>=2:
        await message.answer("Vote limit reached")
        return

    votes.append(now)
    vote_cooldowns[voter]=votes

    async with pool.acquire() as conn:

        if rating=="good":

            await conn.execute("""
            UPDATE users
            SET good=good+1
            WHERE telegram_id=$1
            """,target)

        if rating=="bad":

            await conn.execute("""
            UPDATE users
            SET bad=bad+1
            WHERE telegram_id=$1
            """,target)

        user=await conn.fetchrow("""
        SELECT good FROM users
        WHERE telegram_id=$1
        """,target)

        if user["good"]>=50:

            await conn.execute("""
            UPDATE users
            SET verified=TRUE
            WHERE telegram_id=$1
            """,target)

@dp.message_handler(commands=["report"])
async def report(message:types.Message):

    args=message.text.split()

    if len(args)!=2:
        return

    target=int(args[1])

    async with pool.acquire() as conn:

        await conn.execute("""
        UPDATE users
        SET scam_reports=scam_reports+1
        WHERE telegram_id=$1
        """,target)

        data=await conn.fetchrow("""
        SELECT scam_reports FROM users
        WHERE telegram_id=$1
        """,target)

    if data["scam_reports"]>=3:

        await bot.restrict_chat_member(
            GROUP_ID,
            target,
            permissions=types.ChatPermissions(can_send_messages=False)
        )

        async with pool.acquire() as conn:

            await conn.execute("""
            INSERT INTO blacklist(telegram_id)
            VALUES($1)
            ON CONFLICT DO NOTHING
            """,target)

        await message.answer("⚠ scammer muted")

@dp.message_handler(commands=["admin"])
async def admin(message:types.Message):

    if message.from_user.id!=ADMIN_ID:
        return

    async with pool.acquire() as conn:

        users=await conn.fetchval("SELECT COUNT(*) FROM users")
        invites=await conn.fetchval("SELECT SUM(invites) FROM users")
        scammers=await conn.fetchval("SELECT COUNT(*) FROM blacklist")

    await message.answer(f"""
Admin Dashboard

Users: {users}
Invites: {invites}
Blacklisted: {scammers}
""")

@dp.message_handler(commands=["analytics"])
async def analytics(message:types.Message):

    if message.from_user.id!=ADMIN_ID:
        return

    async with pool.acquire() as conn:

        rows=await conn.fetch("""
        SELECT username,invites
        FROM users
        ORDER BY invites DESC
        LIMIT 5
        """)

    text="Top Inviters\n\n"

    for r in rows:
        text+=f"@{r['username']} — {r['invites']}\n"

    await message.answer(text)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def welcome(message:types.Message):

    for user in message.new_chat_members:

        await message.reply(
        f"Welcome {user.first_name}\nUse /invite to earn rewards"
        )

async def on_startup(dp):
    await connect_db()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
