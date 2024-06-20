"""This file represents a start logic."""

from aiogram import Router, types, html
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from src.db.database import Database
from src.language.translator import LocalizedTranslator
from ..structures.fsm.registration import RegisterGroup
from ..structures.keyboards import common

from src.scraper.parsers.kun_uz import KunUzParser
from src.scraper.parsers.daryo import DaryoUzParser


start_router = Router(name='start')


@start_router.message(CommandStart())
async def start_handler(message: types.Message, db: Database, translator: LocalizedTranslator, state: FSMContext):
    """Start command handler."""
    await state.clear()

    user = await db.user.get_me(message.from_user.id)

    if not user:
        await db.user.new(
            user_id=message.from_user.id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
            second_name=message.from_user.last_name,
            is_premium=bool(message.from_user.is_premium)
        )
        await db.session.commit()

    await message.answer(
        "Assalomu aleykum. Yangiliklar mavzusini tanlang",
        reply_markup=common.show_categories()
    )

