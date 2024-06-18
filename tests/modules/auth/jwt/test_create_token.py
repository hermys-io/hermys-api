from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time
from jose import jwt

from hermys.modules.auth.jwt import create_token
from hermys.settings import get_settings

settings = get_settings()


@pytest.mark.anyio
def test_create_token():
    data_to_encode = {
        'foo': 'foo',
        'bar': 'bar',
    }

    token = create_token(data=data_to_encode)

    decoded_token = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )

    assert token
    assert 'foo' in decoded_token
    assert 'bar' in decoded_token


@freeze_time('2024-01-01 12:00:00')
@pytest.mark.anyio
def test_create_token_default_expires():
    data_to_encode = {
        'foo': 'foo',
        'bar': 'bar',
    }

    token = create_token(data=data_to_encode)

    decoded_token = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )
    expectedExpeires = datetime.now() + timedelta(minutes=15)

    assert 'exp' in decoded_token
    assert decoded_token['exp'] == expectedExpeires.timestamp()


@freeze_time('2024-01-01 12:00:00')
@pytest.mark.anyio
def test_create_token_with_custom_expires():
    data_to_encode = {
        'field01': 'field01',
        'field02': 'field02',
    }

    token = create_token(
        data=data_to_encode,
        expires_delta=timedelta(minutes=30),
    )

    decoded_token = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )
    expectedExpeires = datetime.now() + timedelta(minutes=30)

    assert 'exp' in decoded_token
    assert decoded_token['exp'] == expectedExpeires.timestamp()
