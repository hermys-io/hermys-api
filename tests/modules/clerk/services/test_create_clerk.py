import pytest
from bson import ObjectId

from hermys.db.base import ObjectIdField
from hermys.modules.clerk.enums import OpenAiGPTModelEnum
from hermys.modules.clerk.exceptions import ClerkAlreadyExists
from hermys.modules.clerk.schemas import ClerkCreatePayload, ClerkDBO
from hermys.modules.clerk.services.create_clerk import (
    CreateClerkService,
    get_create_clerk_service,
)


@pytest.mark.anyio
async def test_create_clerk(mocker):
    # Repository mock
    dbo_mock_input = ClerkDBO(
        slug='my-clerk',
        name='My clerk',
        description='My Clerk description',
        prompt='You are a helpful assistant.',
        gpt_model=OpenAiGPTModelEnum.GPT_4o_MINI,
        chat_title='Clerk',
        photo_light=None,
        photo_dark=None,
        active=True,
        deleted_at=None,
    )
    dbo_mock_output = dbo_mock_input.model_copy()
    dbo_mock_output.id = ObjectIdField(ObjectId())

    clerk_repo_mock = mocker.Mock()
    clerk_repo_mock.exists = mocker.AsyncMock(return_value=False)
    clerk_repo_mock.create = mocker.AsyncMock(return_value=dbo_mock_output)

    # Audit mock
    audit_service_mock = mocker.Mock()
    audit_service_mock.dispatch_non_blocking = mocker.AsyncMock()

    service = CreateClerkService(
        clerk_repo=clerk_repo_mock,
        audit_service=audit_service_mock,
    )

    payload = ClerkCreatePayload(
        name='My clerk',
        description='My Clerk description',
        prompt='You are a helpful assistant.',
        gpt_model=OpenAiGPTModelEnum.GPT_4o_MINI,
        chat_title='Clerk',
    )

    current_user_mock = mocker.Mock()
    current_user_mock.id = ObjectId()
    current_user_mock.username = 'test@email.com'

    clerk = await service.dispatch(
        payload=payload,
        current_user=current_user_mock,
    )

    assert clerk
    clerk_repo_mock.create.assert_called_once_with(dbo=dbo_mock_input)
    audit_service_mock.dispatch_non_blocking.assert_called_once()


@pytest.mark.anyio
async def test_cant_create_clerk_with_same_slug(
    mocker,
):
    # Repository mock
    dbo_mock_input = ClerkDBO(
        slug='my-clerk',
        name='My clerk',
        description='My Clerk description',
        prompt='You are a helpful assistant.',
        gpt_model=OpenAiGPTModelEnum.GPT_4o_MINI,
        chat_title='Clerk',
        photo_light=None,
        photo_dark=None,
        active=True,
        deleted_at=None,
    )
    dbo_mock_output = dbo_mock_input.model_copy()
    dbo_mock_output.id = ObjectIdField(ObjectId())

    clerk_repo_mock = mocker.Mock()
    clerk_repo_mock.exists = mocker.AsyncMock(return_value=True)
    clerk_repo_mock.create = mocker.AsyncMock(return_value=dbo_mock_output)

    # Audit mock
    audit_service_mock = mocker.Mock()
    audit_service_mock.dispatch_non_blocking = mocker.AsyncMock()

    service = CreateClerkService(
        clerk_repo=clerk_repo_mock,
        audit_service=audit_service_mock,
    )

    payload = ClerkCreatePayload(
        name='My clerk',
        description='My Clerk description',
        prompt='You are a helpful assistant.',
        gpt_model=OpenAiGPTModelEnum.GPT_4o_MINI,
        chat_title='Clerk',
    )

    current_user_mock = mocker.Mock()
    current_user_mock.id = ObjectId()
    current_user_mock.username = 'test@email.com'

    with pytest.raises(ClerkAlreadyExists):
        await service.dispatch(
            payload=payload,
            current_user=current_user_mock,
        )


@pytest.mark.anyio
def test_service_function(mocker):
    mock_clerk_repo = mocker.Mock()
    mock_audit_service = mocker.Mock()

    service = get_create_clerk_service(
        clerk_repo=mock_clerk_repo, audit_service=mock_audit_service
    )

    assert isinstance(service, CreateClerkService)

    assert service.clerk_repo == mock_clerk_repo
    assert service.audit_service == mock_audit_service
