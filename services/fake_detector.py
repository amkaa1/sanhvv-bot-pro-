from database import cursor

def is_fake(user):

    # Bot check
    if user.is_bot:
        return True

    # Duplicate check
    cursor.execute(
        "SELECT user_id FROM users WHERE user_id=?",
        (user.id,)
    )

    if cursor.fetchone():
        return True

    return False
