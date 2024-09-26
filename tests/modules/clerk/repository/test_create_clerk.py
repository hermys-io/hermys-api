import pytest
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.clerk.enums import OpenAiGPTModelEnum
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.schemas import ClerkDBO


@pytest.mark.anyio
async def test_create_clerk(shared_db: AsyncIOMotorDatabase):
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

    result = await repo.create(dbo=dbo)

    assert isinstance(result, ClerkDBO)
    assert isinstance(result.id, ObjectId)
    assert result.model_dump(exclude={'id'}) == dbo.model_dump(exclude={'id'})
