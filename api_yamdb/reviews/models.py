from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"
    CHOICES_ROLE = [(USER, "user"), (MODERATOR, "moderator"), (ADMIN, "admin")]

    username = models.CharField(
        "Имя пользователя",
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r"^[\w.@+-]+\Z")],
        help_text=(
            "Required. 150 characters or fewer."
            "Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField("E-mail", max_length=254, unique=True)
    first_name = models.CharField("Имя", max_length=150, blank=True)
    last_name = models.CharField("Фамилия", max_length=150, blank=True)
    bio = models.TextField("Биография", blank=True)
    role = models.CharField(
        "Статус пользователя",
        choices=CHOICES_ROLE,
        max_length=30,
        default=USER,
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
    def __str__(self) -> str:
        return self.username


class Category(models.Model):
class Category(models.Model):
    name = models.CharField(
        max_length=256, unique=True,
        verbose_name="Наименование категории"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
<<<<<<< HEAD
        verbose_name="Адрес_страницы",
=======
        verbose_name="Адрес страницы",
        validators=[RegexValidator(regex=r"^[-a-zA-Z0-9_]+$")],
>>>>>>> develop
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
    def __str__(self) -> str:
        return self.name


<<<<<<< HEAD
class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        verbose_name="Наименование жанра"
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Адрес_страницы",
=======
class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name="Наименование жанра")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Адрес страницы",
        verbose_name="Адрес страницы",
        validators=[RegexValidator(regex=r"^[-a-zA-Z0-9_]+$")],
>>>>>>> develop
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self) -> str:
    def __str__(self) -> str:
        return self.name


class Title(models.Model):
class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование произведения"
    )
    year = models.PositiveSmallIntegerField(
        verbose_name="Год выпуска"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        Genre,
        related_name="titles",
        verbose_name="Жанр",
    )
    category = models.ForeignKey(
        Category,
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="titles",
        verbose_name="Категория",
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self) -> str:
    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Модель для отзывов."""

    text = models.TextField("Текст отзыва")
    title = models.ForeignKey(
        Title,
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Произведение",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        "Оценка", validators=[MinValueValidator(1), MaxValueValidator(10)]
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

    text = models.TextField("Текст комментария")
    pub_date = models.DateTimeField(
        "Дата публикации", auto_now_add=True, db_index=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Отзыв",
        help_text="Отзыв, к которому оставлен комментарий",
    )
<<<<<<< HEAD
    # title = models.ForeignKey(
    #     Titles,
    #     on_delete=models.CASCADE,
    #     related_name="comments",
    #     verbose_name="Произведение",
    # )
=======
>>>>>>> develop
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
    )

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]
