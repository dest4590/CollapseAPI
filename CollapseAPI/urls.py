from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from clients.api import *
from clients.serializers import router

schema_view = get_schema_view(
    openapi.Info(
        title="CollapseAPI",
        default_version="v1",
        description="API documentation for CollapseAPI, a platform for secure minecraft clients.",
        terms_of_service="https://collapseloader.org/terms-of-usage/",
        contact=openapi.Contact(email="admin@collapseloader.org"),
        license=openapi.License(name="GPL 3.0 License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("", include(router.urls)),
    path("api/client/<int:client_id>/launch", client_launch, name="client_launch"),
    path(
        "api/client/<int:client_id>/download", client_download, name="client_download"
    ),
    path("api/loader/launch", loader_launch, name="loader_launch"),
    path("admin/", admin.site.urls),
    # SWAG $$$
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
