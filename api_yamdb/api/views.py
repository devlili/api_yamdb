from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .permissions import (
    IsAdminModeratorAuthorPermission,
    IsAdminPermission,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
)


# class UserViewSet(viewsets.ModelViewSet):
#     """Вьюсет для объектов модели User."""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsOwnerOrAdmin,)
#     filter_backends = (SearchFilter,)
#     search_fields = ("username",)
#     lookup_field = "username"
#     http_method_names = [
#         "get",
#         "post",
#         "patch",
#         "delete",
#         "head",
#         "options",
#         "trace",
#     ]
#
#     @action(
#         methods=["get", "patch"],
#         detail=False,
#         url_path="me",
#         permission_classes=(IsAuthenticated,),
#     )
#     def get_patch_me(self, request):
#         user = get_object_or_404(User, username=self.request.user)
#         if request.method == "GET":
#             serializer = MeSerializer(user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         if request.method == "PATCH":
#             serializer = MeSerializer(user, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для получения списка жанров и категорий;
    создания и удаления жанров и категорий"""
    pass


class GenreViewSet(ListCreateDeleteViewSet):
    """Вьюсет для объектов модели Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAdminPermission,)


class CategoryViewSet(ListCreateDeleteViewSet):
    """Вьюсет для объектов модели Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    permission_classes = (IsAdminPermission,)


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Title."""

    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminPermission, IsAuthenticatedOrReadOnly)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleCreateSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title_id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorPermission,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


# def validate_user_data_and_get_response(username, email):
#     serializer = UserSerializer(data={"username": username, "email": email})
#     serializer.validate({"username": username, "email": email})
#     serializer.is_valid(True)
#
#
# @api_view(["POST"])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     email = serializer.validated_data["email"]
#     username = serializer.validated_data["username"]
#     validate_user_data_and_get_response(username, email)
#     try:
#         user, create = User.objects.get_or_create(
#             username=username, email=email
#         )
#     except IntegrityError:
#         return Response(
#             "Такой логин или email уже существуют",
#             status=status.HTTP_400_BAD_REQUEST,
#         )
#     confirmation_code = str(uuid.uuid4())
#     user.confirmation_code = confirmation_code
#     user.save()
#     send_mail(
#         "Код подверждения",
#         confirmation_code,
#         EMAIL,
#         (email,),
#         fail_silently=False,
#     )
#     return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# @api_view(["POST"])
# def get_token(request):
#     serializer = TokenSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     username = serializer.validated_data["username"]
#     confirmation_code = serializer.validated_data["confirmation_code"]
#     user_base = get_object_or_404(User, username=username)
#     if confirmation_code == user_base.confirmation_code:
#         token = str(AccessToken.for_user(user_base))
#         return Response({"token": token}, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
