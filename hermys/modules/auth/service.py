from datetime import timedelta

from hermys.modules.auth.exceptions import (
    IncorrectUsernameOrPassword,
    Unauthorized,
)
from hermys.modules.auth.jwt import create_token, decode_token
from hermys.modules.auth.password import verify_password
from hermys.modules.auth.schemas import AccessTokenData, LoginCredentialPayload
from hermys.modules.user.repository import UserRepository


class AuthService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo
        self.access_token_expiration = timedelta(days=30)

    async def get_token(self, *, login_credentials: LoginCredentialPayload):
        user = await self.user_repo.get(
            by='username',
            value=login_credentials.username,
        )

        if not user or not verify_password(
            login_credentials.password,
            user.password,
        ):
            raise IncorrectUsernameOrPassword()

        access_token_data = AccessTokenData(
            id=user.id,
            username=user.username,
            role=user.role,
            organization=user.organization,
            active=user.active,
        )

        return create_token(
            data=access_token_data.model_dump(),
            expires_delta=self.access_token_expiration,
        )

    async def get_current_user(self, *, access_token: str):
        decoded_data = decode_token(token=access_token)
        token_data = AccessTokenData.model_validate(decoded_data)

        user = await self.user_repo.get(
            by='username',
            value=token_data.username,
        )

        if not user:
            raise Unauthorized()

        return user
