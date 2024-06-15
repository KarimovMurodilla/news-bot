from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.database import Database
from src.configuration import conf


class AdminFilter(BaseFilter):
    async def __call__(self, message: Message, *args, **kwargs):
        if message.from_user.id in conf.ADMINS:
            return True
