import pytest
from bson import ObjectId
from fastapi.testclient import TestClient

from hermys.db.base import ObjectIdField
from hermys.main import app
from hermys.modules.auth.dependencies import get_current_user
from hermys.modules.clerk.enums import OpenAiGPTModelEnum
from hermys.modules.clerk.schemas import ClerkCreatePayload, ClerkRetrieve
from hermys.modules.clerk.services.create_clerk import get_create_clerk_service


@pytest.mark.anyio
async def test_create_clerk(mocker, client: TestClient, fastapi_dep):
    clerk_id = ObjectId()
    mock_service = mocker.AsyncMock()
    mock_service.dispatch.return_value = ClerkRetrieve(
        _id=ObjectIdField(clerk_id),
        slug='clerk-test',
        name='Clerk Test',
        description='A test clerk',
        chat_title='Chat Title Test',
    )

    mock_current_user = mocker.AsyncMock()
    mock_current_user.id = ObjectId()
    mock_current_user.username = 'test@email.com'

    payload = {
        'name': 'Clerk Test',
        'description': 'A test clerk',
        'prompt': 'Test prompt',
        'gpt_model': OpenAiGPTModelEnum.GPT_4o_MINI,
        'chat_title': 'Chat Title Test',
    }

    with fastapi_dep(app).override(
        {
            get_create_clerk_service: lambda: mock_service,
            get_current_user: lambda: mock_current_user,
        }
    ):
        response = client.post(
            '/clerk',
            json=payload,
            headers={'Authorization': 'Bearer test_token'},
        )
        response_data = response.json()

        assert response.status_code == 201
        assert response_data == {
            'id': str(clerk_id),
            'slug': 'clerk-test',
            'name': 'Clerk Test',
            'description': 'A test clerk',
            'chat_title': 'Chat Title Test',
            'photo_light': None,
            'photo_dark': None,
            'active': True,
        }
        mock_service.dispatch.assert_called_once_with(
            current_user=mock_current_user,
            payload=ClerkCreatePayload.model_validate(payload),
        )
