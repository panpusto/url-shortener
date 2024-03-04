from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from app.models import URL, URLCreate
from app.crud import crud_urls as crud


@pytest.fixture(name="session")
def session_fixture() -> Generator:
    engine = create_engine(
        url=settings.sync_database_url,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator:
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="url_dict")
def url_dict_fixture(client: TestClient) -> dict:
    response = client.post(
        "/urls",
        json={"target_url": "http://example.com"}
    )
    data = response.json()
    return data


@pytest.fixture(name="url_obj")
def url_obj_fixture(session: Session) -> URL:
    url = URLCreate(target_url="http://example.com/")
    url_data = crud.create_db_url(session, url)
    return url_data
