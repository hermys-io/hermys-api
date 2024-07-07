from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.knowledge.exceptions import KnowledgeNotFound
from hermys.modules.knowledge.schemas import (
    KnowledgeCreatePayload,
    KnowledgeRetrieve,
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

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

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
