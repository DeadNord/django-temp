from rest_framework import serializers

from .models import Item


class PingResponseSerializer(serializers.Serializer):
    """Example of a DRF serializer for the HealthService response."""

    message = serializers.CharField(read_only=True, help_text="Should be 'pong'.")


class ItemSerializer(serializers.ModelSerializer):
    """Serializer for the demo ``Item`` model."""

    class Meta:
        model = Item
        fields = ["id", "name", "description"]

