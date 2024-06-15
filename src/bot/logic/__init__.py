"""This package is used for a bot logic implementation."""
from .help import help_router
from .start import start_router
from .news.categories import news_router

routers = (start_router, help_router, news_router,)
