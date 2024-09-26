import pytest
from pydantic import ValidationError

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.schemas import UserCreatePayload, UserRetrieve
from hermys.modules.user.service import UserService


@pytest.mark.anyio
async def test_create(user_service: UserService):
    payload = UserCreatePayload(
        username='teste@email.com',
        password='12345Aa@',  # noqa: S106
        organization='hermys',
        role=UserRoleEnum.ADMIN,
    )
    create_user = await user_service.create(payload=payload)

    assert create_user
    assert isinstance(create_user, UserRetrieve)


@pytest.mark.anyio
async def test_cant_create_god_user(user_service: UserService):
    with pytest.raises(ValidationError):
        payload = UserCreatePayload(
            username='teste@email.com',
            password='12345Aa@',  # noqa: S106
            organization='hermys',
            role=UserRoleEnum.GOD,
        )
        await user_service.create(payload=payload)
