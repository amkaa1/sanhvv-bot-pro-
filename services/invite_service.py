from database import cursor, conn
from services.leaderboard_service import update_leaderboard

async def add_invite(inviter_id, bot):

    cursor.execute(
        "UPDATE users SET invites = invites + 1 WHERE user_id=?",
        (inviter_id,)
    )

    conn.commit()

    await update_leaderboard(bot)
