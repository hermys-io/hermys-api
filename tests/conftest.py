from typing import Optional, Protocol
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from hermys.db.shared_db import get_shared_db
from hermys.main import app
from hermys.modules.auth.service import AuthService
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload, UserInternal
from hermys.modules.user.service import UserService
from hermys.settings import get_settings

settings = get_settings()


async def get_shared_db_override():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client['t-shared']

    try:
        yield db
    finally:
        collections = await db.list_collection_names()
        for collection in collections:
            await db.drop_collection(collection)

        client.close()


app.dependency_overrides[get_shared_db] = get_shared_db_override


@pytest.fixture()
async def client():
    return TestClient(app)


@pytest.fixture()
async def shared_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client['t-shared']

    try:
        yield db
    finally:
        collections = await db.list_collection_names()
        for collection in collections:
            await db.drop_collection(collection)

        client.close()


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
def user_repository(shared_db: AsyncIOMotorDatabase):
    return UserRepository(db=shared_db)


@pytest.fixture
def user_service(user_repository: UserRepository):
    return UserService(user_repo=user_repository)


class CreateUserFunc(Protocol):
    async def __call__(
        self, *, organization: Optional[str], role: Optional[UserRoleEnum]
    ) -> UserInternal:
        ...


@pytest.fixture
def create_user(user_repository: UserRepository):
    async def func(
        *,
        organization: Optional[str] = None,
        role: Optional[UserRoleEnum] = None,
    ):
        payload = UserCreatePayload(
            username=f'{uuid4()}@email.com',
            organization=organization if organization else 'acme',
            role=role if role else UserRoleEnum.ADMIN,
            password='12345Aa@',  # noqa: S106
        )
        return await user_repository.create(payload=payload)

    return func


@pytest.fixture
def auth_service(user_repository: UserRepository):
    return AuthService(user_repo=user_repository)
