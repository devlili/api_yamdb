from django.contrib import admin

from .models import Comment, Rating, Review


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
