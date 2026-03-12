from database import cursor, conn

def add_invite(inviter_id):

    cursor.execute(
        "UPDATE users SET invites = invites + 1 WHERE user_id=?",
        (inviter_id,)
    )

    conn.commit()
