from fastapi.datastructures import URL as fa_URL
from sqlmodel import Session

from app.models import URL, URLCreate, URLRead
from app.utils.keygen import create_random_key, create_unique_random_key
from app.core.config import settings
from app.api.api_v1.endpoints import urls


def create_db_url(db: Session, url: URLCreate):
    key = create_unique_random_key(db)
    secret_key = f"{key}_{create_random_key(length=8)}"
    db_url = URL(
        target_url=str(url.target_url), key=key, secret_key=secret_key
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def get_db_url_by_key(db: Session, url_key: str) -> URL:
    return (
        db.query(URL)
        .filter(URL.key == url_key, URL.is_active)
        .first()
    )


def get_db_url_by_secret_key(db: Session, secret_key: str) -> URL:
    return (
        db.query(URL)
        .filter(URL.secret_key == secret_key, URL.is_active)
        .first()
    )


def get_admin_info(db_url: URL) -> URLRead:
    base_url = fa_URL(settings.base_url)
    admin_endpoint = urls.router.url_path_for(
        "administration info", secret_key=db_url.secret_key
    )
    url = str(base_url.replace(path=db_url.key))
    admin_url = str(base_url.replace(path=admin_endpoint))

    url_info = URLRead(
        target_url=db_url.target_url,
        url=url,
        admin_url=admin_url,
        is_active=db_url.is_active,
        clicks=db_url.clicks
    )
    return url_info


def update_db_clicks(db: Session, db_url: URL) -> URL:
    db_url.clicks += 1
    db.commit()
    db.refresh(db_url)
    return db_url


def deactivate_db_url_by_secret_key(db: Session, secret_key: str) -> URL:
    db_url = get_db_url_by_secret_key(db, secret_key)
    if db_url:
        db_url.is_active = False
        db.commit()
        db.refresh(db_url)
    return db_url
