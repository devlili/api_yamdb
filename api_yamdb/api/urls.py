from django.urls import include, path
from api.views import CategoriesViewSet, TitlesViewSet, GenresViewSet, CommentViewSet, ReviewViewSet
from rest_framework import routers

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('categories', CategoriesViewSet)
router_v1.register('genres', GenresViewSet)
router_v1.register('titles', TitlesViewSet)
router_v1 = routers.DefaultRouter()
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comments",
)
router_v1.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="reviews"
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
