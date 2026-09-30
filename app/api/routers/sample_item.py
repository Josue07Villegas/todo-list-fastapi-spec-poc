from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.repositories.sample_item_repository import SampleItemRepository
from app.schemas.sample_item import SampleItemCreateRequest, SampleItemResponse
from app.services.sample_item_service import SampleItemService

router = APIRouter(prefix="/sample-items", tags=["sample"])


def get_sample_item_service(db: Session = Depends(get_db)) -> SampleItemService:
    return SampleItemService(SampleItemRepository(db))


@router.post("", response_model=SampleItemResponse, status_code=201)
def create_sample_item(
    payload: SampleItemCreateRequest,
    service: SampleItemService = Depends(get_sample_item_service),
) -> SampleItemResponse:
    # Router = capa delgada: solo parsea/valida via schema, delega en el
    # service y devuelve la respuesta. Sin SQL ni reglas de negocio aqui.
    item = service.create_item(payload.name)
    return SampleItemResponse.model_validate(item)


@router.get("", response_model=list[SampleItemResponse])
def list_sample_items(
    service: SampleItemService = Depends(get_sample_item_service),
) -> list[SampleItemResponse]:
    items = service.list_items()
    return [SampleItemResponse.model_validate(item) for item in items]
