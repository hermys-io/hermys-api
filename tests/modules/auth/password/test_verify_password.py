import pytest

from hermys.modules.auth.password import get_hashed_password, verify_password


@pytest.mark.anyio
def test_verify_password():
    password = '12345Aa@'  # noqa: S105
    hashed_password = get_hashed_password(password)

    assert verify_password(password, hashed_password) is True


@pytest.mark.anyio
def test_verify_password_wrong_password():
    password = '12345Aa@'  # noqa: S105
    hashed_password = get_hashed_password(password)

    assert verify_password('wrong password', hashed_password) is False
