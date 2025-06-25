# api/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from .serializers import ItemSerializer, PingResponseSerializer
from .services.ItemService import ItemService
from .services.HealthService import HealthService


class PingView(APIView):
    """GET /api/temp/ping/ → {"message": "pong"}."""

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "global"

    @extend_schema(
        responses={200: PingResponseSerializer},
        description="Health-check endpoint to verify that the API is alive.",
        summary="Ping",
        tags=["System"],
    )
    def get(self, request):
        data = HealthService().ping()
        serializer = PingResponseSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/temp/items/  → список Item
    POST /api/temp/items/  → создать Item
    """

    serializer_class = ItemSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "global"

    # ---------- READ ----------
    def get_queryset(self):
        return ItemService().list_items()

    # ---------- CREATE --------
    def perform_create(self, serializer):
        ItemService().create_item(**serializer.validated_data)

    # ---------- docs ----------
    @extend_schema(
        tags=["Item"],
        summary="List & Create items",
        description=(
            "GET возвращает все объекты.\n\n"
            "POST создаёт новый Item и возвращает его в теле ответа."
        ),
        request=ItemSerializer,  # тело POST
        responses={
            200: ItemSerializer(many=True),  # ответ на GET
            201: ItemSerializer,  # ответ на POST
        },
        examples=[
            OpenApiExample(
                "Create item",
                value={"name": "Sample", "description": "first item"},
                request_only=True,
            ),
            OpenApiExample(
                "Created response",
                value={"id": 1, "name": "Sample", "description": "first item"},
                response_only=True,
            ),
        ],
    )
    def get(self, *args, **kwargs):
        """Хук, чтобы DRF-Spectacular увидел кастомную аннотацию."""
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
