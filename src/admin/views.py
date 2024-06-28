from fastapi import Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqladmin import ModelView, BaseView, expose
from wtforms.fields import SelectField

from .settings import Session, engine

from ..db.models import (
    User, News, Category, 
    Source, Url, View
)


class UserAdmin(ModelView, model=User):
    column_list = [User.user_id, User.user_name, User.first_name, User.second_name, User.is_active]
    can_create = False
    can_edit = True
    can_delete = False
    icon = "fa-solid fa-users"
    name_plural = "Users"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class NewsAdmin(ModelView, model=News):
    column_list = [
        News.title, News.url, News.date,
    ]
    column_searchable_list = [News.title, News.url, News.date]
    column_sortable_list = [News.title, News.url, News.date]
    page_size = 100

    icon = "fa-solid fa-news"
    name_plural = "News"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class CategoryAdmin(ModelView, model=Category):
    column_list = [
        Category.id, Category.name,
    ]
    icon = "fa-solid fa-category"
    name_plural = "Categories"
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
    

class SourceAdmin(ModelView, model=Source):
    column_list = [
        Source.id, Source.url, Source.created_at,
    ]
    icon = "fa-solid fa-news"
    name_plural = "Sources"
    page_size = 100
    
    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True


class UrlAdmin(ModelView, model=Url):
    column_list = [
        Url.url, Url.category_id, Url.language, Url.source_id, Url.created_at, 
    ]
    
    icon = "fa-solid fa-news"
    name_plural = "Urls"

    form_include_columns = [
        Url.url, Url.category_id, Url.source_id, Url.language,
    ]

    form_excluded_columns = [
        Url.created_at,
    ]

    def is_visible(self, request: Request) -> bool:
        return True

    def is_accessible(self, request: Request) -> bool:
        return True
    
    async def scaffold_form(self) -> dict:
        form = await super().scaffold_form()
        async with AsyncSession(engine) as session:
            categories = await session.execute(select(Category))
            sources = await session.execute(select(Source))

            category_choices = [(int(category.id), category.name) for category in categories.scalars().all()]
            source_choices = [(int(source.id), source.url) for source in sources.scalars().all()]

            form.category_id = SelectField('Category', choices=category_choices)
            form.source_id = SelectField('Source', choices=source_choices)

        return form

    async def on_model_change(self, data: dict, model, is_created: bool, request: Request):
        async with AsyncSession(engine) as session:
            data['category_id'] = int(data['category_id'])
            data['source_id'] = int(data['source_id'])

            if model is None:  # Если модель не существует (т.е. создание новой записи)
                model = self.model()  # Создаем новый экземпляр модели

            model.url = data['url']
            model.category_id = data['category_id']
            model.source_id = data['source_id']
            model.language = data['language']
            
            if is_created:
                session.add(model)
            return await session.commit()

