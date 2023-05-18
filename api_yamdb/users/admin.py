from django.contrib import admin
from reviews.models import User


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
