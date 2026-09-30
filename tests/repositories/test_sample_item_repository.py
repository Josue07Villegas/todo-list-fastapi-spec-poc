from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import Base
from app.repositories.sample_item_repository import SampleItemRepository


def make_session() -> Session:
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_create_and_list_persist_via_sqlite() -> None:
    db = make_session()
    repository = SampleItemRepository(db)

    repository.create("primer item")
    repository.create("segundo item")

    items = repository.list()
    assert [i.name for i in items] == ["primer item", "segundo item"]


def test_get_returns_none_when_missing() -> None:
    db = make_session()
    repository = SampleItemRepository(db)

    assert repository.get(999) is None
