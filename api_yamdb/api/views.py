from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Comment, Review, Title

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return Comment.objects.filter(
            title=self.get_title(), review=self.get_review()
        )

    # self.get_title().get_review().comments.all() надо подумать

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
            review=self.get_review(),
        )


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для объектов модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )
