from typing import Annotated

from fastapi import Depends

from hermys.db.dependencies import GetSharedDB
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.service import UserService


def get_shared_user_repository(shared_db: GetSharedDB):
    return UserRepository(db=shared_db)


GetSharedUserRepository = Annotated[
    UserRepository,
    Depends(get_shared_user_repository),
]


def get_shared_user_service(shared_user_repo: GetSharedUserRepository):
    return UserService(user_repo=shared_user_repo)


GetSharedUserService = Annotated[
    UserService,
    Depends(get_shared_user_service),
]
