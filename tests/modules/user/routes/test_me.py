import pytest
from fastapi.testclient import TestClient

from hermys.modules.auth.schemas import LoginCredentialPayload
from hermys.modules.auth.service import AuthService
from tests.conftest import CreateUserFunc


@pytest.mark.anyio
async def test_me(
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

    response = client.get(
        '/user/me',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert 'username' in response.json()
    assert 'role' in response.json()
    assert 'organization' in response.json()


@pytest.mark.anyio
async def test_me_without_credentials(client: TestClient):
    response = client.get(
        '/user/me',
    )

    assert response.status_code == 401
    assert 'detail' in response.json()
    assert 'code' in response.json()
