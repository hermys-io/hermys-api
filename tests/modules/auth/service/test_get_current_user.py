import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.db.base import ObjectIdField
from hermys.modules.auth.exceptions import Unauthorized
from hermys.modules.auth.jwt import create_token
from hermys.modules.auth.schemas import AccessTokenData, LoginCredentialPayload
from hermys.modules.auth.service import AuthService
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload


@pytest.mark.anyio
async def test_get_current_user(shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    auth_service = AuthService(user_repo=user_repo)
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='test',
        role=UserRoleEnum.GOD,
    )
    await user_repo.create(payload=payload)

    login_credentials = LoginCredentialPayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
    )
    access_token = await auth_service.get_token(
        login_credentials=login_credentials,
    )

    current_user = await auth_service.get_current_user(
        access_token=access_token
    )

    assert current_user
    assert current_user.username == 'email@email.com'


@pytest.mark.anyio
async def test_get_current_unknow_user(shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    auth_service = AuthService(user_repo=user_repo)

    access_token_data = AccessTokenData(
        id=ObjectIdField(ObjectId()),
        username='unknow@email.com',
        role='admin',
        organization='hermys',
        active=True,
    )
    access_token = create_token(data=access_token_data.model_dump())

    with pytest.raises(Unauthorized):
        await auth_service.get_current_user(access_token=access_token)
