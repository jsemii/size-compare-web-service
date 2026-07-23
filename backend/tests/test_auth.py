from jose import jwt

from app.core.config import settings
from app.services.security import (
    hash_password,
    verify_password,
    create_access_token,
)


def test_hash_password_is_not_plain():
    hashed = hash_password("mypassword")
    assert hashed != "mypassword"


def test_hash_password_is_random():
    first = hash_password("mypassword")
    second = hash_password("mypassword")
    assert first != second


def test_verify_password_correct():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) is True


def test_verify_password_wrong():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) is False


def test_create_access_token_contains_user_id():
    token = create_access_token(1)
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )
    assert payload["sub"] == "1"


def test_create_access_token_has_expire():
    token = create_access_token(1)
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )