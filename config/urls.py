import os
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("api/temp/", include("api.urls")),
    # Схема OpenAPI
    path("api/temp/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path(
        "api/temp/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # Redoc
    path(
        "api/temp/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
