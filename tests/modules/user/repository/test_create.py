import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.exceptions import UserAlreadyExists
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload


@pytest.mark.anyio
async def test_create_user(shared_db: AsyncIOMotorDatabase):
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='hermys',
        role=UserRoleEnum.ADMIN,
    )

    repo = UserRepository(db=shared_db)
    created_user = await repo.create(payload=payload)

    assert created_user.id
    assert created_user.username
    assert created_user.organization
    assert created_user.role
    assert created_user.password
    assert created_user.active is False


@pytest.mark.anyio
async def test_user_already_exists(shared_db: AsyncIOMotorDatabase):
    payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='hermys',
        role=UserRoleEnum.ADMIN,
    )

    repo = UserRepository(db=shared_db)
    await repo.create(payload=payload)

    with pytest.raises(UserAlreadyExists):
        await repo.create(payload=payload)
