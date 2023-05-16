from django.core import validators
from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title, User


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
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
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                "Оценкой может быть целое число в диапазоне от 1 до 10."
            )
        return value


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для объектов модели User."""

    email = serializers.EmailField(
        max_length=254, validators=(validators.MaxLengthValidator(254),)
    )
    username = serializers.SlugField(
        max_length=150,
        validators=(
            validators.MaxLengthValidator(150),
            validators.RegexValidator(r"^[\w.@+-]+\Z"),
        ),
    )

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get("email")).exists():
            user = User.objects.get(email=attrs.get("email"))
            if user.username != attrs.get("username"):
                raise serializers.ValidationError(
                    "Такой адрес электронной почты уже зарегестрирован"
                )
        if User.objects.filter(username=attrs.get("username")).exists():
            user = User.objects.get(username=attrs.get("username"))
            if user.email != attrs.get("email"):
                raise serializers.ValidationError(
                    "Пользователь с таким именем уже зарегестрирован"
                )
        return super().validate(attrs)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "role",
            "bio",
            "first_name",
            "last_name",
        )
        lookup_field = "username"
        extra_kwargs = {
            "username": {"required": True},
            "email": {"required": True},
        }


class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(max_length=150, required=True)

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    def validate(self, data):
        username = data.get("username")
        email = data.get("email")
        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise serializers.ValidationError(
                "Пользователь с таким именем уже зарегестрирован"
            )
        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise serializers.ValidationError(
                "Такой адрес электронной почты уже зарегестрирован"
            )
        return data

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")
