from django.core import validators
from rest_framework import serializers

from users.models import User


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
                    {"error": "Email уже используется"}
                )
        if User.objects.filter(username=attrs.get("username")).exists():
            user = User.objects.get(username=attrs.get("username"))
            if user.email != attrs.get("email"):
                raise serializers.ValidationError(
                    {"error": "Имя пользователя уже используется"}
                )
        return super().validate(attrs)

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
    """Сериализатор для регистрации нового пользователя."""

    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(
            validators.RegexValidator(r"^[\w.@+-]+\Z"),)
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value

    def validate(self, data):
        username = User.objects.filter(username=data['username']).exists()
        email = User.objects.filter(email=data['email']).exists()
        if email and not username:
            raise serializers.ValidationError('400')
        if username and not email:
            raise serializers.ValidationError('400')
        return data

    class Meta:
        model = User
        fields = (
            "username",
            "email",
        )


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code")


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор для учетных данных."""

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
