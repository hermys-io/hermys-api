import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload


@pytest.mark.anyio
async def test_token(client: TestClient, shared_db: AsyncIOMotorDatabase):
    user_repo = UserRepository(db=shared_db)
    user_payload = UserCreatePayload(
        username='email@email.com',
        password='12345Aa@',  # noqa: S106
        organization='test',
        role=UserRoleEnum.GOD,
    )
    await user_repo.create(payload=user_payload)

    payload = {'username': 'email@email.com', 'password': '12345Aa@'}
    response = client.post('/auth/token', json=payload)

    assert response.status_code == 200
    assert 'access_token' in response.json()


@pytest.mark.anyio
async def test_token_unknow_user(client: TestClient):
    payload = {'username': 'unknow@email.com', 'password': '12345Aa@'}
    response = client.post('/auth/token', json=payload)

    assert response.status_code == 422
