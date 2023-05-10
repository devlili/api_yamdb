from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Categories, Comment, Genres, Review, Titles


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        field = ("name", "slug")
        lookup_field = "slug"


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        field = ("name", "slug")
        lookup_field = "slug"


# class TitlesBaseSerializer(serializers.ModelSerializer):
#     rating = serializers.IntegerField()
#     genre = GenresSerializer(read_only=True, many=True)
#     category = CategoriesSerializer(read_only=True)

#     class Meta:
#         model = Titles
#         fields = (
#             "id",
#             "name",
#             "year",
#             "rating",
#             "description",
#             "genre",
#             "category",
#         )


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Titles
        fields = ("id", "name", "year", "description", "genre", "category")

        def get_rating(self, obj):
            return (
                int(
                    Review.objects.filter(title=self).aggregate(Avg("score"))[
                        "score__avg"
                    ]
                )
                or None
            )

    def validate_year(self, value):
        current_year = timezone.now().year
        if 0 < value > current_year:
            raise serializers.ValidationError("Год выпуска введен неверно.")
        return value


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Comment."""

    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "pub_date")
        model = Comment
        read_only_fields = ("id", "author", "pub_date")


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Review."""

    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review
        read_only_fields = ("id", "author", "pub_date")

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=("author", "title"),
                message="Вы уже оставили отзыв на это произведение.",
            )
        ]
