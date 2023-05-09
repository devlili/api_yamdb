from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Rating(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="rating",
        verbose_name="Произведение",
    )

    @property
    def average_rating(self):
        return (int(
            Review.objects.filter(title=self).aggregate(models.Avg("score"))[
                "score__avg"
            ])
            or None
        )

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f"{self.title.name}: {self.rate}"


class Review(models.Model):
    """Модель для отзывов."""

    text = models.TextField("Текст отзыва")
    title = models.ForeignKey(
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
        "Оценка", validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(score__range=(1, 10)), name="valid_score"
            ),
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
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Произведение",
    )
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
