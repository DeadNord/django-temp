from rest_framework import serializers


class PingResponseSerializer(serializers.Serializer):
    """Example of a DRF serializer for the HealthService response."""

    message = serializers.CharField(read_only=True, help_text="Should be 'pong'.")