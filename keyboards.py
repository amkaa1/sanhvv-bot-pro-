from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton("👤 Profile", callback_data="profile")
    )

    kb.add(
        InlineKeyboardButton("🏆 Leaderboard", callback_data="top")
    )

    kb.add(
        InlineKeyboardButton("🎁 Invite Friends", callback_data="invite")
    )

    return kb
