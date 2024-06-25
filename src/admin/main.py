#!/usr/bin/env python3

from fastapi import FastAPI
from sqladmin import Admin

from .auth import AdminAuth
from .settings import engine
from ..configuration import conf

from .views import (
    UserAdmin, NewsAdmin, CategoryAdmin,
    SourceAdmin, UrlAdmin, ViewAdmin, SimilarsAdmin
)

app = FastAPI()
authentication_backend = AdminAuth(secret_key=conf.SECRET_KEY)
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend, templates_dir='src/admin/templates')


admin.add_view(UserAdmin)
admin.add_view(NewsAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(SourceAdmin)
admin.add_view(UrlAdmin)
admin.add_view(ViewAdmin)
admin.add_view(SimilarsAdmin)
