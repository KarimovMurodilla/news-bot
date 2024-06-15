"""Database class with all-in-one features."""

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine

from src.configuration import conf

from .repositories import (
    UserRepo, NewsRepo, ViewRepo,
    CategoryRepo, SourceRepo, UrlRepo,
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    """Create async engine with given URL.

    :param url: URL to connect
    :return: AsyncEngine
    """
    return _create_async_engine(url=url, echo=conf.debug, pool_pre_ping=True)


class Database:
    """Database class.

    is the highest abstraction level of database and
    can be used in the handlers or any others bot-side functions.
    """

    user: UserRepo
    news: NewsRepo
    view: ViewRepo
    category: CategoryRepo
    source: SourceRepo
    url: UrlRepo

    session: AsyncSession

    def __init__(
        self,
        session: AsyncSession,
        user: UserRepo = None,
        news: NewsRepo = None,
        view: ViewRepo = None,
        category: CategoryRepo = None,
        source: SourceRepo = None,
        url: UrlRepo = None
    ):
        """Initialize Database class.

        :param session: AsyncSession to use
        """
        self.session = session
        self.user = user or UserRepo(session=session)
        self.news = news or NewsRepo(session=session)
        self.view = view or ViewRepo(session=session)
        self.category = category or CategoryRepo(session=session)
        self.source = source or SourceRepo(session=session)
        self.url = url or UrlRepo(session=session)
