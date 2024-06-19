from typing import Annotated, Union

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from hermys.modules.auth.exceptions import Unauthorized
from hermys.modules.auth.service import AuthService
from hermys.modules.user.dependencies import GetSharedUserRepository
from hermys.modules.user.schemas import UserInternal

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service(user_repo: GetSharedUserRepository):
    return AuthService(user_repo=user_repo)


GetAuthService = Annotated[
    AuthService,
    Depends(get_auth_service),
]


def get_access_token(
    auth: Annotated[
        Union[HTTPAuthorizationCredentials, None],
        Depends(bearer_scheme),
    ],
):
    if not auth:
        raise Unauthorized()

    return auth.credentials


GetAccessToken = Annotated[str, Depends(get_access_token)]


async def get_current_user(
    access_token: GetAccessToken,
    auth_service: GetAuthService,
):
    return await auth_service.get_current_user(access_token=access_token)


GetCurrentUser = Annotated[UserInternal, Depends(get_current_user)]
