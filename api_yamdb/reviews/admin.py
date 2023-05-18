from django.contrib import admin
from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("slug",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("slug",)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "year",
        "description",
        "category",
    )
    search_fields = ("name",)
    list_filter = ("year",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "review", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "score", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)
