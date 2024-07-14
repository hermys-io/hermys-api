from typing import Annotated
from urllib.parse import urlparse

from fastapi import Depends, Request


def get_host_name(request: Request):
    referer = request.headers.get('referer')
    if not referer:
        raise Exception()

    return urlparse(referer).netloc.split(':')[0]


GetHostName = Annotated[
    str,
    Depends(get_host_name),
]
