from sqlmodel import create_engine

from app.core.config import settings


engine = create_engine(
    url=settings.sync_database_url,
    echo=settings.db_echo_log
)
