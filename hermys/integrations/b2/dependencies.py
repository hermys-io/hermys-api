from typing import Annotated

from fastapi import Depends

from hermys.integrations.b2.integration import B2Integration


def get_b2_integration():
    return B2Integration()


GetB2Integration = Annotated[B2Integration, Depends(get_b2_integration)]
