import secrets
import string

from sqlmodel import Session

from app.crud import crud_urls


def create_random_key(length: int = 5) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))


def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    while crud_urls.get_db_url_by_key(db, key):
        key = create_random_key()
    return key
