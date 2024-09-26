from typing import Literal, TypeAlias, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.clerk.exceptions import ClerkNotFound
from hermys.modules.clerk.schemas import ClerkDBO, ClerkUpdatePayload

ClerkGetBy: TypeAlias = Union[Literal['_id'], Literal['slug']]
ClerkGetValue: TypeAlias = Union[str, ObjectId]


class ClerkRepository:
    collection_name = 'clerk'

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[self.collection_name]

    async def create(
        self,
        *,
        dbo: ClerkDBO,
    ) -> ClerkDBO:
        data_to_insert = dict(dbo)

        result = await self.collection.insert_one(data_to_insert)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def update(self, *, clerk_id: ObjectId, payload: ClerkUpdatePayload):
        payload_dict = payload.model_dump(exclude_none=True)
        await self.collection.update_one(
            {'_id': clerk_id}, {'$set': payload_dict}
        )

        return await self.get_or_rise(by='_id', value=clerk_id)

    async def get(
        self,
        *,
        by: ClerkGetBy,
        value: ClerkGetValue,
    ) -> Union[ClerkDBO, None]:
        result = await self.collection.find_one({by: value})

        return ClerkDBO.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: ClerkGetBy,
        value: ClerkGetValue,
    ) -> ClerkDBO:
        result = await self.collection.find_one({by: value})

        if result:
            return ClerkDBO.model_validate(result)

        raise ClerkNotFound()

    async def exists(self, *, by: ClerkGetBy, value: ClerkGetValue) -> bool:
        result = await self.collection.find_one({by: value})

        return bool(result)
