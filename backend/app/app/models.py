from typing import Optional

from pydantic import AnyUrl, BaseModel
from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel


class URLBase(SQLModel):
    target_url: str


class URL(URLBase, UUIDModel, TimestampModel, table=True):
    __tablename__ = "urls"

    key: str = Field(unique=True, index=True)
    secret_key: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)
    clicks: int = Field(default=0)


class URLCreate(BaseModel):
    target_url: AnyUrl


class URLRead(URLBase):
    url: str
    admin_url: str
    is_active: bool
    clicks: int
