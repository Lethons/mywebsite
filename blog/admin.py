from django.contrib import admin
from .models import Tag, Blog

# Register your models here.
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tag', 'publish_time', 'update_time')
    list_per_page = 20
    list_filter = ('tag',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
    list_per_page = 20
