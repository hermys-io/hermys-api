import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload


@pytest.mark.anyio
async def test_get_by_id(shared_db: AsyncIOMotorDatabase):
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='hermys',
        role=UserRoleEnum.ADMIN,
    )

    repo = UserRepository(db=shared_db)
    created_user = await repo.create(payload=payload)

    object_from_db = await repo.get(by='_id', value=created_user.id)

    assert object_from_db


@pytest.mark.anyio
async def test_get_by_email(shared_db: AsyncIOMotorDatabase):
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='hermys',
        role=UserRoleEnum.ADMIN,
    )

    repo = UserRepository(db=shared_db)
    await repo.create(payload=payload)

    object_from_db = await repo.get(by='username', value=payload.username)

    assert object_from_db


@pytest.mark.anyio
async def test_get_none_return(shared_db: AsyncIOMotorDatabase):
    repo = UserRepository(db=shared_db)

    object_from_db = await repo.get(by='username', value='unknow')

    assert object_from_db is None
