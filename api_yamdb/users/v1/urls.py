from django.urls import include, path
from rest_framework import routers

from users.v1 import views
from users.v1.views import UserViewSet

app_name = "users"

router_v1 = routers.DefaultRouter()
router_v1.register("users", UserViewSet, basename="users")

urlpatterns = [
    path("v1/", include(router_v1.urls)),
    path("v1/auth/signup/", views.signup, name="token_get"),
    path(
        "v1/auth/token/",
        views.get_token,
        name="token_send",
    ),
]
