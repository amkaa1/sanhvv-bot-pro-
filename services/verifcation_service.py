from database import cursor

def already_joined(user_id):

    cursor.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchone() is not None
