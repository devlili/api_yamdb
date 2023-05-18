from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from users.models import User


class Category(models.Model):
    """Модель для категории."""

    name = models.CharField(
        max_length=256, unique=True, verbose_name="Наименование категории"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Адрес_страницы",
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель для жанра."""

    name = models.CharField(
        max_length=256, unique=True, verbose_name="Наименование жанра"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Адрес страницы",
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель для произведения."""

    def year_validator(value):
        if value < 0 or value > timezone.now().year:
            raise ValidationError(
                "%(value)s is not a correcrt year!",
                params={"value": value},
            )

    name = models.CharField(
        max_length=256, verbose_name="Наименование произведения"
    )
    year = models.PositiveSmallIntegerField(
        validators=[year_validator], verbose_name="Год выпуска"
    )
    description = models.TextField(verbose_name="Описание", blank=True)
    genre = models.ManyToManyField(
        Genre,
        through="Genre_title",
        related_name="titles",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="titles",
        null=True,
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
        return self.name


class Genre_title(models.Model):
    """Модель для жанра произведения."""

    title = models.ForeignKey(
        Title,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="titles",
        verbose_name="Произведение",
    )
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="genres",
        verbose_name="Жанр",
    )

    class Meta:
        verbose_name = "Жанр произведения"
        verbose_name_plural = "Жанры произведения"
        constraints = [
            models.UniqueConstraint(
                fields=["title", "genre"], name="unique_combination"
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.genre}"


class Review(models.Model):
    """Модель для отзывов."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    text = models.TextField("Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    score = models.IntegerField(
        "Оценка", validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["author", "title"], name="review_once"
            ),
        ]
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель для комментариев."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
        help_text="Отзыв, к которому оставлен комментарий",
    )
    text = models.TextField("Текст комментария")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]
