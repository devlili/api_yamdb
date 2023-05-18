from uuid import uuid4

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.v1.permissions import IsOwnerOrAdmin
from api_yamdb.settings import EMAIL
from users.models import User
from users.serializers import (
    MeSerializer,
    SignupSerializer,
    TokenSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели User."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = [
        "get",
        "post",
        "patch",
        "delete",
    ]

    @action(
        methods=["get", "patch"],
        detail=False,
        url_path="me",
        permission_classes=(IsAuthenticated,),
    )
    def get_patch_me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == "GET":
            serializer = MeSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data["email"]
    username = serializer.validated_data["username"]
    user, create = User.objects.get_or_create(username=username, email=email)
    confirmation_code = str(uuid4())
    user.confirmation_code = confirmation_code
    user.save()
    send_mail(
        "Код подверждения",
        confirmation_code,
        EMAIL,
        (email,),
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    confirmation_code = serializer.validated_data["confirmation_code"]
    user_base = get_object_or_404(User, username=username)
    if confirmation_code == user_base.confirmation_code:
        token = str(AccessToken.for_user(user_base))
        return Response({"token": token}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
