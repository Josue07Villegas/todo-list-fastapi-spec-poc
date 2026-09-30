import pytest

from app.models.sample_item import SampleItem
from app.services.exceptions import DuplicateSampleItemError
from app.services.sample_item_service import SampleItemService


class FakeSampleItemRepository:
    """Repositorio falso en memoria: el service se testea sin tocar la
    base de datos real, tal como pide spec_estandares_modelo_datos.txt
    seccion 3 ('Inyeccion de dependencias' / 'Pruebas en espejo')."""

    def __init__(self) -> None:
        self._items: list[SampleItem] = []
        self._next_id = 1

    def create(self, name: str) -> SampleItem:
        item = SampleItem(id=self._next_id, name=name)
        self._next_id += 1
        self._items.append(item)
        return item

    def list(self) -> list[SampleItem]:
        return list(self._items)


def test_create_item_happy_path() -> None:
    service = SampleItemService(FakeSampleItemRepository())

    item = service.create_item("  primer item  ")

    assert item.name == "primer item"
    assert [i.name for i in service.list_items()] == ["primer item"]


def test_create_item_rejects_duplicates() -> None:
    service = SampleItemService(FakeSampleItemRepository())
    service.create_item("duplicado")

    with pytest.raises(DuplicateSampleItemError):
        service.create_item("duplicado")
