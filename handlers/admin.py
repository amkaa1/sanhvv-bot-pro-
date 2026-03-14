from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import SessionLocal
from handlers.admin_filter import AdminFilter
from handlers.admin_menu import admin_menu
from handlers.stats import build_stats_text


router = Router()
router.message.filter(AdminFilter())


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    await message.answer(
        "🔐 <b>Админ цэс</b>\n\n"
        "Доорх товчуудаас сонгож болно.",
        reply_markup=admin_menu(),
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    async with SessionLocal() as session:  # type: AsyncSession
        text = await build_stats_text(session)
    await message.answer(text)

