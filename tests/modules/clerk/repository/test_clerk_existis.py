import pytest
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.clerk.enums import OpenAiGPTModelEnum
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.schemas import ClerkDBO


@pytest.mark.anyio
async def test_clerk_existis_by_id(shared_db: AsyncIOMotorDatabase):
    repo = ClerkRepository(db=shared_db)
    dbo = ClerkDBO(
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
    created_clerk = await repo.create(dbo=dbo)
    clerk_id = created_clerk.id

    result = await repo.exists(by='_id', value=clerk_id)

    assert result is True


@pytest.mark.anyio
async def test_clerk_existis_by_slug(shared_db: AsyncIOMotorDatabase):
    clerk_slug = 'my-clerk'
    repo = ClerkRepository(db=shared_db)
    dbo = ClerkDBO(
        slug=clerk_slug,
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
    await repo.create(dbo=dbo)

    result = await repo.exists(by='slug', value=clerk_slug)

    assert result is True


@pytest.mark.anyio
async def test_clerk_existis_return_false_if_not_found(
    shared_db: AsyncIOMotorDatabase,
):
    repo = ClerkRepository(db=shared_db)

    result = await repo.exists(by='slug', value='unknown-slug')

    assert result is False
