from django.contrib import admin

from . import models


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'published')


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
