from django.contrib import admin

from .models import Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption', 'author']
    list_display_links = ['caption']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
