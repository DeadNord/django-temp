from typing import Iterable
from ..models import Item


class ItemService:
    """Инкапсулирует всю бизнес-логику, связанную с Item."""

    def list_items(self) -> Iterable[Item]:
        """Вернуть все объекты (можно легко добавить фильтры/пагинацию)."""
        return Item.objects.all()

    def create_item(self, *, name: str, description: str | None = None) -> Item:
        """Создать объект и вернуть его (валидация — на уровне serializer)."""
        return Item.objects.create(name=name, description=description)
