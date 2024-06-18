import pytest

from hermys.modules.auth.password import get_hashed_password


@pytest.mark.anyio
def test_get_hashed_password():
    password = '12345Aa@'  # noqa: S105
    hashed_password = get_hashed_password(password)

    assert hashed_password
    assert hashed_password != password
