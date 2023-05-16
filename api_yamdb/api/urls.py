from api import views
from api.views import (
    CategoryViewSet,
    CommentViewSet,
    GenreViewSet,
    ReviewViewSet,
    TitleViewSet,
    UserViewSet,
)
from django.urls import include, path
from rest_framework import routers


app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register("categories", CategoryViewSet, basename="categories")
router_v1.register("genres", GenreViewSet, basename="genres")
router_v1.register("titles", TitleViewSet, basename="titles")
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path('v1/auth/signup/', views.signup, name="token_get"),
    path('v1/auth/token/', views.get_token, name="token_send",)
]
