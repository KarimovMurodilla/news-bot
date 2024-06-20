"""User repository file."""

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.structures.role import Role

from ..models import Base, User
from .abstract import Repository


class UserRepo(Repository[User]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=User, session=session)

    async def new(
        self,
        user_id: int,
        user_name: str | None = None,
        first_name: str | None = None,
        second_name: str | None = None,
        is_premium: bool | None = False,
        is_active: bool | None = True,
    ) -> None:
        await self.session.merge(
            User(
                user_id=user_id,
                user_name=user_name,
                first_name=first_name,
                second_name=second_name,
                is_premium=is_premium,
                is_active=is_active
            )
        )
        await self.session.commit()

    async def get_me(self, user_id: int) -> User:
        """Get user role by id."""
        return await self.session.scalar(
            select(User).where(User.user_id == user_id).limit(1)
        )
    
    async def get_all_users(self):
        """Get user role by id."""
        result = await self.session.scalars(
            select(User).where(User.is_active == True)
        )
        users = result.all()
        return users

    async def update_user(self, user_id: int, **kwargs) -> User:
        """Update user by id with new data."""
        async with self.session.begin():
            stmt = (
                update(User)
                .where(User.user_id == user_id)
                .values(**kwargs)
            )
            await self.session.execute(stmt)
            await self.session.commit()