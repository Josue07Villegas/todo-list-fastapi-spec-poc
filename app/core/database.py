from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings


class Base(DeclarativeBase):
    pass


# Fallback a SQLite en memoria cuando no hay DATABASE_URL configurada, para
# que el recurso de referencia (sample_item) sea ejecutable sin depender de
# un Postgres real. El dominio real (User/Task) debe usar settings.database_url
# (Postgres) tal como pide la especificacion, no este fallback.
# StaticPool es necesario para SQLite en memoria: sin el, cada nueva Session
# abriria una conexion nueva y por lo tanto una base de datos ":memory:"
# distinta y vacia.
_engine_url = settings.database_url or "sqlite:///:memory:"
_is_sqlite = _engine_url.startswith("sqlite")
_engine_kwargs = {"connect_args": {"check_same_thread": False}, "poolclass": StaticPool} if _is_sqlite else {}

engine = create_engine(_engine_url, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
