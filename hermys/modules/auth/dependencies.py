from typing import Annotated

from fastapi import Depends

from hermys.modules.auth.service import AuthService
from hermys.modules.user.dependencies import GetSharedUserRepository


def get_auth_service(user_repo: GetSharedUserRepository):
    return AuthService(user_repo=user_repo)


GetAuthService = Annotated[
    AuthService,
    Depends(get_auth_service),
]
