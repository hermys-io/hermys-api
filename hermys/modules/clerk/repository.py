from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from slugify import slugify

from hermys.modules.clerk.exceptions import ClerkAlreadyExists, ClerkNotFound
from hermys.modules.clerk.schemas import ClerkCreatePayload, ClerkRetrieve


class ClerkRepository:
    collection_name = 'clerk'

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[self.collection_name]

    async def create(
        self,
        *,
        payload: ClerkCreatePayload,
    ) -> ClerkRetrieve:
        slug = slugify(payload.name)

        if await self.get(by='slug', value=slug):
            raise ClerkAlreadyExists()

        payload_dict = payload.model_dump()
        payload_dict['active'] = True
        payload_dict['slug'] = slug

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[ClerkRetrieve, None]:
        result = await self.collection.find_one({by: value})

        return ClerkRetrieve.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> ClerkRetrieve:
        result = await self.collection.find_one({by: value})

        if result:
            return ClerkRetrieve.model_validate(obj=result)

        raise ClerkNotFound()
