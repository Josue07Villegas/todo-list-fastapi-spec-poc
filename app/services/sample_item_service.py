from app.models.sample_item import SampleItem
from app.repositories.sample_item_repository import SampleItemRepository
from app.services.exceptions import DuplicateSampleItemError


class SampleItemService:
    """Capa de logica de negocio: no conoce objetos HTTP (Request/Response),
    solo tipos de dominio (ver spec_estandares_modelo_datos.txt seccion 3).
    """

    def __init__(self, repository: SampleItemRepository) -> None:
        self.repository = repository

    def create_item(self, name: str) -> SampleItem:
        normalized = name.strip()
        if any(existing.name == normalized for existing in self.repository.list()):
            raise DuplicateSampleItemError(normalized)
        return self.repository.create(normalized)

    def list_items(self) -> list[SampleItem]:
        return self.repository.list()
