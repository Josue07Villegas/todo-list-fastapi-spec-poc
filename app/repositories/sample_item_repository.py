from sqlalchemy.orm import Session

from app.models.sample_item import SampleItem


class SampleItemRepository:
    """Capa de acceso a datos: solo consultas/escrituras, sin logica de
    negocio (ver spec_estandares_modelo_datos.txt seccion 3).
    """

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, name: str) -> SampleItem:
        item = SampleItem(name=name)
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list(self) -> list[SampleItem]:
        return list(self.db.query(SampleItem).order_by(SampleItem.id).all())

    def get(self, item_id: int) -> SampleItem | None:
        return self.db.get(SampleItem, item_id)
