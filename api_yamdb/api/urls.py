from api.views import (
    CategoriesViewSet,
    CommentViewSet,
    GenresViewSet,
    ReviewViewSet,
    TitlesViewSet,
)
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
app_name = "api"

router_v1 = routers.DefaultRouter()
router_v1.register("categories", CategoriesViewSet, basename="categories")
router_v1.register("genres", GenresViewSet, basename="genres")
router_v1.register("titles", TitlesViewSet, basename="titles")
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
    path('api/auth/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', TokenRefreshView.as_view(), name='token_refresh'),
]
