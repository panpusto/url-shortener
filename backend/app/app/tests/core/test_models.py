import uuid
from datetime import datetime

from app.core.models import TimestampModel, UUIDModel


def test_create_uuid_model():
    uuid_obj = UUIDModel()
    assert uuid_obj.id is not None
    assert type(uuid_obj.id) is uuid.UUID


def test_create_timestamp_model():
    timestamp = TimestampModel()
    assert timestamp.created_at is not None
    assert type(timestamp.created_at) is datetime
    assert timestamp.updated_at is not None
    assert type(timestamp.updated_at) is datetime
