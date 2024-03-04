from app.utils.keygen import (
    create_random_key,
    create_unique_random_key
)


def test_create_random_key_default_value():
    key = create_random_key()
    assert len(key) == 5


def test_create_random_key_input_value():
    length = 10
    key = create_random_key(length)
    assert len(key) == length
