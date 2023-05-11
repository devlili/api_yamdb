from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
<<<<<<< HEAD
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator
from reviews.models import Categories, Comment, Genres, Review, Titles
from rest_framework.exceptions import ValidationError
=======
from reviews.models import Category, Comment, Genre, Review, Title
>>>>>>> develop


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Genres
=======
        model = Genre
>>>>>>> develop
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
<<<<<<< HEAD
        model = Categories
=======
        model = Category
>>>>>>> develop
        fields = ("name", "slug")


class TitleReadSerializer(serializers.ModelSerializer):
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
        return round(rating, 1)


class TitleCreateSerializer(serializers.ModelSerializer):
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

<<<<<<< HEAD
    def year_validator(value):
        if value < 0 or value > timezone.now().year:
            raise ValidationError(('%(value)s is not a correcrt year!'),
                                params={'value': value},
                                )
    # def validate_year(self, value):
    #     current_year = timezone.now().year
    #     if not 0 <= value > current_year:
    #         raise serializers.ValidationError(
    #             'Проверьте год создания произведения.'
    #         )
    #     return value
=======
    def validate_year(self, value):
        current_year = timezone.now().year
        if not 0 <= value <= current_year:
            raise serializers.ValidationError(
                "Проверьте год создания произведения."
            )
        return value
>>>>>>> develop


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
        # read_only_fields = ("id", "author", "pub_date")


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
        # read_only_fields = ("id", "author", "pub_date")

    def validate(self, data):
        if self.context.get("request").method != "POST":
            return data
        title = self.context.get("view").kwargs.get("title_id")
        author = self.context.get("request").user
        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                "Вы уже написали отзыв к этому произведению."
            )
<<<<<<< HEAD
        ]


# class ReviewSerializer(serializers.ModelSerializer):
#     author = serializers.SlugRelatedField(
#         read_only=True,
#         slug_field='username'
#     )

#     class Meta:
#         model = Review
#         fields = ('id', 'text', 'author', 'score', 'pub_date')
#         read_only_fields = ('id', 'author', 'pub_date')

#     def validate(self, data):
#         title_id = self.context['view'].kwargs.get('title_id')
#         request = self.context['request']
#         title = get_object_or_404(Title, id=title_id)
#         if request.method == 'POST':
#             if Review.objects.filter(
#                 author=request.user, title=title
#             ).exists():
#                 raise ValidationError(
#                     'Вы ужэе оставили отзыв на это произведение')
#         return data
=======
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Оценкой может быть целое число в диапазоне от 1 до 10.'
            )
        return value
>>>>>>> develop
