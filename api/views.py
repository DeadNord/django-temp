from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import ScopedRateThrottle
from drf_spectacular.utils import extend_schema
from rest_framework import generics

from .serializers import PingResponseSerializer, ItemSerializer
from .models import Item
from .services.HealthService import HealthService


class PingView(APIView):
    """GET /api/ping → {"message": "pong"}.

    A super‑simple endpoint wired through *view → service → serializer* to test
    the stack. Throttling is re‑used from global settings.
    """

    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "global"

    @extend_schema(
        responses={200: PingResponseSerializer},
        description="Health‑check endpoint to verify that the API is alive.",
        summary="Ping",
        tags=["System"],
    )
    def get(self, request):
        data = HealthService().ping()
        serializer = PingResponseSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ItemListCreateView(generics.ListCreateAPIView):
    """List or create ``Item`` objects."""

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

