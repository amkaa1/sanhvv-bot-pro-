from database import cursor
from config import GROUP_ID

LEADERBOARD_MESSAGE_ID = None


async def update_leaderboard(bot):

    cursor.execute(
        "SELECT user_id, invites FROM users ORDER BY invites DESC LIMIT 10"
    )

    users = cursor.fetchall()

    text = "🏆 Invite Leaderboard\n\n"

    for i, u in enumerate(users, start=1):
        text += f"{i}. {u[0]} — {u[1]} invites\n"

    if LEADERBOARD_MESSAGE_ID:

        await bot.edit_message_text(
            text,
            GROUP_ID,
            LEADERBOARD_MESSAGE_ID
        )
