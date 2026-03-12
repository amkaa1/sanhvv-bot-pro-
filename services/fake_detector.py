from datetime import datetime

def is_fake_account(user):

    if user.is_bot:
        return True

    if not user.username:
        return True

    return False
