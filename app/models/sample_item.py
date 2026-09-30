from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class SampleItem(Base):
    """Recurso de referencia: solo demuestra la capa de persistencia
    (models/) del patron arquitectonico. No forma parte del dominio Todo
    List (User/Task); ver spec_estandares_modelo_datos.txt seccion 3 y 4.
    """

    __tablename__ = "sample_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
