from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователя."""

    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    USER_LEVELS = ((USER, "User"), (MODERATOR, "Moderator"), (ADMIN, "Admin"))

    role = models.CharField(
        "Роль", max_length=32, choices=USER_LEVELS, default=USER
    )
    bio = models.TextField("О Себе", max_length=256, blank=True)
    email = models.EmailField("Почта", blank=True, max_length=254)
    confirmation_code = models.CharField(
        "Код подтверждения", max_length=100, null=True
    )

    @property
    def is_admin(self):
        return self.role == User.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == User.MODERATOR

    @property
    def is_user(self):
        return self.role == User.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.username
