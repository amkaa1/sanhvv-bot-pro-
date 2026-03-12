import database

rewards = {
    100:20000,
    500:100000,
    1000:300000,
    2000:600000
}

async def check_rewards(user_id):

    async with database.pool.acquire() as conn:

        user = await conn.fetchrow("""

        SELECT invites FROM users
        WHERE telegram_id=$1

        """, user_id)

        invites = user["invites"]

        for r in rewards:

            if invites >= r:

                await conn.execute("""

                INSERT INTO rewards(user_id,reward_level)
                VALUES($1,$2)
                ON CONFLICT DO NOTHING

                """, user_id, r)
