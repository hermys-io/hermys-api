import pytest

from hermys.modules.user.schemas import UserRetrieve
from hermys.modules.user.service import UserService
from tests.conftest import CreateUserFunc


@pytest.mark.anyio
async def test_list(
    user_service: UserService,
    create_user: CreateUserFunc,
):
    await create_user(organization='hermys', role=None)
    await create_user(organization='hermys', role=None)

    results = await user_service.list(organization='hermys')

    assert len(results) == 2
    assert isinstance(results[0], UserRetrieve)


@pytest.mark.anyio
async def test_list_empty(user_service: UserService):
    results = await user_service.list(organization='hermys')

    assert len(results) == 0
