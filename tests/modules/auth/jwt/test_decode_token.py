from datetime import timedelta

import pytest
from freezegun import freeze_time

from hermys.modules.auth.exceptions import Unauthorized
from hermys.modules.auth.jwt import create_token, decode_token
from hermys.settings import get_settings

settings = get_settings()


@pytest.mark.anyio
def test_decode_token():
    data_to_encode = {
        'foo': 'foo',
        'bar': 'bar',
    }

    token = create_token(data=data_to_encode)

    decoded_data = decode_token(token=token)

    assert token
    assert 'foo' in decoded_data
    assert 'bar' in decoded_data


@pytest.mark.anyio
def test_decode_unkow_token():
    token = 'unknow'  # noqa: S105

    with pytest.raises(Unauthorized):
        decode_token(token=token)


@freeze_time('2024-01-01 12:00:00')
@pytest.mark.anyio
def test_decode_expired_token():
    data_to_encode = {
        'foo': 'foo',
        'bar': 'bar',
    }

    token = create_token(
        data=data_to_encode,
        expires_delta=timedelta(minutes=5),
    )

    with freeze_time('2024-01-01 12:30:00'):
        with pytest.raises(Unauthorized):
            decode_token(token=token)
