from django.db.models import Avg, PositiveSmallIntegerField
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from reviews.models import Category, Comment, Genre, Review, Title

from .permissions import IsAdminModeratorAuthorPermission, IsAdminPermission
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReadSerializer,
)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminPermission,)
    search_fields = ("name",)

    def retrieve(self, request, slug=None):
        if not Genre.objects.filter(slug=slug).count():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().retrieve(self, request, slug)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def retrieve(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug=None):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")
    permission_classes = (IsAdminPermission,)

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return TitleCreateSerializer
        return TitleReadSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

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
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )
