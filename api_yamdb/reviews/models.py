from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class ValidateCharacter(RegexValidator):
    pass


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES_ROLE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    ]

    username = models.CharField(
        max_length=150,
        validators=[ValidateCharacter(regex='^[\w.@+-]+\z')],
        unique=True,
        verbose_name='Имя пользователя',
        help_text=('Required. 150 characters or fewer.'
                   'Letters, digits and @/./+/-/_ only.')
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='E-mail')
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        blank=True)
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        blank=True)
    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )
    role = models.CharField(
        verbose_name='Пользовательские роли',
        choices=CHOICES_ROLE,
        max_length=30,
        default=USER
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
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def ___str__(self) -> str:
        return self.username


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование категории')
    slug = models.SlugField(
        max_length=50,
        #validators='^[-a-zA-Z0-9_]+$',
        validators=[ValidateCharacter(regex='^[-a-zA-Z0-9_]+$')],
        unique=True,
        verbose_name='Адрес_страницы')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def ___str__(self) -> str:
        return self.name


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование жанра')
    slug = models.SlugField(
        max_length=50,
       # validators='^[-a-zA-Z0-9_]+$',
        validators=[ValidateCharacter(regex='^[-a-zA-Z0-9_]+$')],
        unique=True,
        verbose_name='Адрес_страницы')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def ___str__(self) -> str:
        return self.name


class Titles(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование произведения')
    year = models.PositiveSmallIntegerField(
        verbose_name='Год выпуска')
    rating = models.IntegerField(verbose_name='Рейтинг', blank=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Жанр')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def ___str__(self) -> str:
        return self.name


class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Username пользователя', related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], 
        verbose_name='Оценка')
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(verbose_name='Дата публикации отзыва', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_relations'),
        )

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='Username автора комментария')
    pub_date = models.DateTimeField(verbose_name='Дата публикации комментария', auto_now_add=True, db_index=True)
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
