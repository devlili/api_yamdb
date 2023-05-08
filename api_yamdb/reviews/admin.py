from django.contrib import admin

from .models import Comment, Review


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "title", "review", "author")
    search_fields = ("text",)
    list_filter = ("pub_date",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "title", "author", "score")
    search_fields = ("text",)
    list_filter = ("pub_date",)
