from django.urls import include, path
from api.views import CategoriesViewSet, TitlesViewSet, GenresViewSet
from rest_framework import routers

app_name = 'api'

v1_router = routers.DefaultRouter()
v1_router.register('categories', CategoriesViewSet)
v1_router.register('genres', GenresViewSet)
v1_router.register('titles', TitlesViewSet)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
