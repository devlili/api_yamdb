from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("api/", include("api.v1.urls", namespace="api")),
    path("api/", include("users.v1.urls", namespace="users")),
    path("admin/", admin.site.urls),
    path(
        "redoc/",
        TemplateView.as_view(template_name="redoc.html"),
        name="redoc",
    ),
]
