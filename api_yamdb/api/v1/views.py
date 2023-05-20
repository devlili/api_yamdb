from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title

from .filters import TitleFilter
from .permissions import IsAdminModeratorAuthorPermission, IsAdminPermission
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
)


class ListCreateDeleteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для получения списка жанров и категорий;
    создания и удаления жанров и категорий."""

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

    queryset = Title.objects.annotate(rating=Avg("reviews__score")).all()
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
