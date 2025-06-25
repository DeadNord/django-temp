from django.db import models


class Item(models.Model):
    """Simple model for demo purposes."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


__all__ = ["Item"]
