from django.contrib import admin
from reviews.models import Genres, Categories, Titles, Comment, Rating, Review


admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Titles)


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "title", "review", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "score", "title", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")  # добавить рейтинг
    search_fields = ("title",)
    list_filter = ("",)  # добавить рейтинг
