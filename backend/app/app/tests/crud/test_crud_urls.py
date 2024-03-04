from sqlmodel import Session

from app.crud import crud_urls as crud
from app.models import URL, URLCreate
from app.core.config import settings


def test_create_db_url(session: Session):
    url = "http://example.com/"
    url_object = URLCreate(target_url=url)
    url_data = crud.create_db_url(session, url_object)
    assert url_data.target_url == url
    assert url_data.created_at is not None
    assert url_data.updated_at is not None
    assert url_data.id is not None
    assert url_data.key is not None
    assert url_data.secret_key is not None
    assert url_data.is_active is True
    assert url_data.clicks == 0


def test_get_db_url_by_key(session: Session, url_obj: URL):
    url_by_key_data = crud.get_db_url_by_key(session, url_obj.key)
    assert url_obj is url_by_key_data


def test_get_db_url_by_key_invalid(session: Session):
    url_by_key_data = crud.get_db_url_by_key(session, "fake_key")
    assert url_by_key_data is None


def test_get_db_url_by_secret_key(session: Session, url_obj: URL):
    url_by_secret_key_data = crud.get_db_url_by_secret_key(session, url_obj.secret_key)
    assert url_obj == url_by_secret_key_data


def test_get_db_url_by_secret_key_invalid(session: Session):
    url_by_secret_key_data = crud.get_db_url_by_secret_key(session, "fake_secret_key")
    assert url_by_secret_key_data is None


def test_get_admin_info(session: Session, url_obj: URL):
    admin_info = crud.get_admin_info(url_obj)
    assert admin_info.target_url == url_obj.target_url
    assert admin_info.url == (settings.base_url + '/' + url_obj.key)
    assert admin_info.admin_url == (settings.base_url + '/admin/' + url_obj.secret_key)
    assert admin_info.is_active is True
    assert admin_info.clicks == 0


def test_update_db_clicks(session: Session, url_obj: URL):
    assert url_obj.clicks == 0
    crud.update_db_clicks(session, url_obj)
    assert url_obj.clicks == 1


def test_deactivate_db_url_by_secret_key(session: Session, url_obj: URL):
    assert url_obj.is_active is True
    crud.deactivate_db_url_by_secret_key(session, url_obj.secret_key)
    assert url_obj.is_active is False
