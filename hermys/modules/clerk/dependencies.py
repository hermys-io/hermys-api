from typing import Annotated

from fastapi import Depends

from hermys.db.db import GetDB
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.service import ClerkService


def get_shared_clerk_repository(db: GetDB):
    return ClerkRepository(db=db)


GetClerkRepository = Annotated[
    ClerkRepository,
    Depends(get_shared_clerk_repository),
]


def get_shared_clerk_service(
    clerk_repo: GetClerkRepository,
):
    return ClerkService(clerk_repo=clerk_repo)


GetClerkService = Annotated[
    ClerkService,
    Depends(get_shared_clerk_service),
]
