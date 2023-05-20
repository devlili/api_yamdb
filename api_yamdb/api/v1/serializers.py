from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, Title


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Genre."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Category."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Title на чтение."""

    rating = serializers.SerializerMethodField()
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg("score")).get("score__avg")
        if not rating:
            return rating
        return round(rating)


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Title на добавление."""

    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
        )


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Comment."""

    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Review."""

    author = SlugRelatedField(
        read_only=True,
        slug_field="username",
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review

    def validate(self, data):
        if self.context.get("request").method != "POST":
            return data
        title = self.context.get("view").kwargs.get("title_id")
        author = self.context.get("request").user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                "Вы уже написали отзыв к этому произведению."
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Оценкой может быть целое число в диапазоне от 1 до 10."
            )
        return value
