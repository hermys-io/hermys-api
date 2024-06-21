import pytest

from hermys.modules.user.repository import UserRepository
from tests.conftest import CreateUserFunc


@pytest.mark.anyio
async def test_list(
    user_repository: UserRepository,
    create_user: CreateUserFunc,
):
    await create_user(organization='hermys', role=None)
    await create_user(organization='hermys', role=None)

    results = await user_repository.list(organization='hermys')

    assert len(results) == 2


@pytest.mark.anyio
async def test_list_empty(user_repository: UserRepository):
    results = await user_repository.list(organization='hermys')

    assert len(results) == 0
