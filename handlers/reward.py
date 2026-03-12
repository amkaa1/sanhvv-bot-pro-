from aiogram import types
import database

rewards = {
    100: 20000,
    500: 100000,
    1000: 300000,
    2000: 600000
}

def register(dp):

    @dp.message_handler(commands=["rewards"])
    async def rewards_info(message: types.Message):

        text = """
🎁 Invite Rewards

100 invites → 20,000₮
500 invites → 100,000₮
1000 invites → 300,000₮
2000 invites → 600,000₮

Reward авах бол:
t.me/n3v3rmor31
"""

        await message.answer(text)


async def check_rewards(user_id):

    async with database.pool.acquire() as conn:

        user = await conn.fetchrow("""

        SELECT invites
        FROM users
        WHERE telegram_id=$1

        """, user_id)

        if not user:
            return

        invites = user["invites"]

        for r in rewards:

            if invites >= r:

                await conn.execute("""

                INSERT INTO rewards(user_id,reward_level)
                VALUES($1,$2)
                ON CONFLICT DO NOTHING

                """, user_id, r)
