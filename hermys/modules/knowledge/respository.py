from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.knowledge.exceptions import KnowledgeNotFound
from hermys.modules.knowledge.schemas import (
    KnowledgeCreatePayload,
    KnowledgeRetrieve,
    KnowledgeUpdatePayload,
)


class KnowledgeRepository:
    collection_name = 'knowledge'

    def __init__(self, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[self.collection_name]

    async def create(
        self,
        *,
        payload: KnowledgeCreatePayload,
    ) -> KnowledgeRetrieve:
        payload_dict = dict(payload)
        payload_dict['photo'] = None

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def update(
        self,
        *,
        clerk_id: ObjectId,
        payload: KnowledgeUpdatePayload,
    ) -> KnowledgeRetrieve:
        payload_dict = payload.model_dump(exclude_none=True)
        await self.collection.update_one(
            {'_id': clerk_id}, {'$set': payload_dict}
        )

        return await self.get_or_rise(by='_id', value=clerk_id)

    async def list(self, *, clerk_id: ObjectId):
        default_filter = {
            'clerk': clerk_id,
            'active': True,
        }
        results = await self.collection.find(default_filter).to_list(None)
        return [KnowledgeRetrieve.model_validate(result) for result in results]

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[KnowledgeRetrieve, None]:
        result = await self.collection.find_one({by: value})

        return KnowledgeRetrieve.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> KnowledgeRetrieve:
        result = await self.collection.find_one({by: value})

        if result:
            return KnowledgeRetrieve.model_validate(result)

        raise KnowledgeNotFound()
