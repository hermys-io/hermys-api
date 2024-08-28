import pytest
from fastapi import Request
from starlette.datastructures import Headers

from hermys.common.host_name_dependencies import get_host_name


def test_get_host_name_with_referer():
    headers = Headers({'referer': 'http://example.com/some/path'})
    request = Request(scope={'type': 'http', 'headers': headers.raw})

    hostname = get_host_name(request)
    assert hostname == 'example.com'


def test_get_host_name_without_referer():
    headers = Headers({})
    request = Request(scope={'type': 'http', 'headers': headers.raw})

    # TODO: Ajustar exceção customizada
    with pytest.raises(Exception):  # noqa: B017
        get_host_name(request)
