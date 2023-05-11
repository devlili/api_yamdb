from django.contrib import admin
from reviews.models import Categories, Comment, Genres, Review, Titles, User


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("slug",)


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("slug",)


@admin.register(Titles)
class TitlesAdmin(admin.ModelAdmin):
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
    list_display = ("pk", "text", "title", "review", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "score", "title", "author", "pub_date")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
        "bio",
        "role",
    )
    search_fields = ("username", "email")
    list_filter = ("role",)
