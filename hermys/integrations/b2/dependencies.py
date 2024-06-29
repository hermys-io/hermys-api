from typing import Annotated

from fastapi import Depends

from hermys.integrations.b2.service import B2Service


def get_b2_service():
    return B2Service()


GetB2Service = Annotated[B2Service, Depends(get_b2_service)]
