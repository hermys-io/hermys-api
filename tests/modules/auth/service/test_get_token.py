import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.auth.exceptions import IncorrectUsernameOrPassword
from hermys.modules.auth.schemas import LoginCredentialPayload
from hermys.modules.auth.service import AuthService
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload


@pytest.mark.anyio
async def test_get_token(shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    auth_service = AuthService(user_repo=user_repo)
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='test',
        role=UserRoleEnum.ADMIN,
    )
    await user_repo.create(payload=payload)

    login_credentials = LoginCredentialPayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
    )
    access_token = await auth_service.get_token(
        login_credentials=login_credentials,
    )

    assert access_token


@pytest.mark.anyio
async def test_get_token_wrong_password(shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    auth_service = AuthService(user_repo=user_repo)
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='test',
        role=UserRoleEnum.ADMIN,
    )
    await user_repo.create(payload=payload)

    login_credentials = LoginCredentialPayload(
        username='email@email.com',
        password='wrong password',  # noqa: S106
    )

    with pytest.raises(IncorrectUsernameOrPassword):
        await auth_service.get_token(
            login_credentials=login_credentials,
        )


@pytest.mark.anyio
async def test_get_token_unknow_user(shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    auth_service = AuthService(user_repo=user_repo)

    login_credentials = LoginCredentialPayload(
        username='unknow@email.com',
        password='wrong password',  # noqa: S106
    )

    with pytest.raises(IncorrectUsernameOrPassword):
        await auth_service.get_token(
            login_credentials=login_credentials,
        )
