from sqlmodel import SQLModel

from .engine import engine


def create_db():
    SQLModel.metadata.create_all(engine)
