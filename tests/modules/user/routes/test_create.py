import pytest
from fastapi.testclient import TestClient

from hermys.modules.auth.schemas import LoginCredentialPayload
from hermys.modules.auth.service import AuthService
from hermys.modules.user.enums import UserRoleEnum
from tests.conftest import CreateUserFunc


@pytest.mark.anyio
async def test_create(
    client: TestClient,
    auth_service: AuthService,
    create_user: CreateUserFunc,
):
    user = await create_user(organization='hermys', role=None)

    login_credentials = LoginCredentialPayload(
        username=user.username,
        password='12345Aa@',  # noqa: S106
    )

    token = await auth_service.get_token(login_credentials=login_credentials)

    payload = {
        'username': 'email@email.com',
        'organization': 'hermys',
        'role': 'user',
        'password': '12345Aa@',
    }
    response = client.post(
        '/user',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 201
    assert 'username' in response.json()
    assert 'role' in response.json()
    assert 'organization' in response.json()


@pytest.mark.anyio
async def test_create_duplicated_user(
    client: TestClient,
    auth_service: AuthService,
    create_user: CreateUserFunc,
):
    user = await create_user(organization='hermys', role=None)

    login_credentials = LoginCredentialPayload(
        username=user.username,
        password='12345Aa@',  # noqa: S106
    )

    token = await auth_service.get_token(login_credentials=login_credentials)

    payload = {
        'username': user.username,
        'organization': 'hermys',
        'role': 'user',
        'password': '12345Aa@',
    }
    response = client.post(
        '/user',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 409
    assert 'detail' in response.json()
    assert 'code' in response.json()


@pytest.mark.anyio
async def test_normal_user_cant_create_user(
    client: TestClient,
    auth_service: AuthService,
    create_user: CreateUserFunc,
):
    user = await create_user(organization='hermys', role=UserRoleEnum.USER)

    login_credentials = LoginCredentialPayload(
        username=user.username,
        password='12345Aa@',  # noqa: S106
    )

    token = await auth_service.get_token(login_credentials=login_credentials)

    payload = {
        'username': 'email@email.com',
        'organization': 'hermys',
        'role': 'user',
        'password': '12345Aa@',
    }
    response = client.post(
        '/user',
        json=payload,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 403
    assert 'detail' in response.json()
    assert 'code' in response.json()
