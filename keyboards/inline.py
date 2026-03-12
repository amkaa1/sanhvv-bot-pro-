from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("Profile", callback_data="profile"),
        InlineKeyboardButton("Invite", callback_data="invite")
    )

    kb.add(
        InlineKeyboardButton("Leaderboard", callback_data="leaderboard")
    )

    return kb
