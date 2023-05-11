from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Categories, Comment, Genres, Review, Titles


class GenresSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=256)
    # slug = serializers.SlugField(max_length=50)

    class Meta:
        model = Genres
        field = ("name", "slug")
        lookup_field = "slug"


class CategoriesSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=256)
    # slug = serializers.SlugField(max_length=50)

    class Meta:
        model = Categories
        field = ("name", "slug")
        lookup_field = "slug"


class TitlesBaseSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField()
    genre = GenresSerializer(read_only=True, many=True)
    category = CategoriesSerializer(read_only=True)

    class Meta:
        model = Titles
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class TitlesPostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True, slug_field="slug", queryset=Genres.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Categories.objects.all()
    )

    class Meta:
        model = Titles
        fields = ("id", "name", "year", "description", "genre", "category")

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
#       read_only_fields = ('id', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели Review."""

    author = SlugRelatedField(read_only=True, slug_field="username")

    class Meta:
        fields = ("id", "text", "author", "score", "pub_date")
        model = Review


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
