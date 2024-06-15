"""Repositories module."""
from .user import UserRepo
from .news import NewsRepo
from .view import ViewRepo
from .category import CategoryRepo
from .source import SourceRepo
from .url import UrlRepo


__all__ = ( 'UserRepo', 'NewsRepo', 'ViewRepo', 'CategoryRepo', 'SourceRepo', 'UrlRepo', )
