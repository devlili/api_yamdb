from django.contrib import admin
from reviews.models import Genres, Categories, Titles

admin.register(Genres)
admin.register(Categories)
admin.register(Titles)


class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name', 'slug',)
    list_filter = ('name', 'slug',)


class TitlesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'name', 'year', 'rating', 'description', 'genre', 'category'
    )
    search_fields = ('category', 'genre', 'name', 'year',)
    list_filter = ('category', 'genre', 'name', 'year',)
