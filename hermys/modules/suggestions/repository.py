from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.suggestions.exceptions import SuggestionNotFound
from hermys.modules.suggestions.schemas import (
    SuggestionCreatePayload,
    SuggestionRetrieve,
)


class SuggestionRepository:
    collection_name = 'suggestion'

    def __init__(self, *, db: AsyncIOMotorDatabase):
        self.collection = db[self.collection_name]

    async def create(self, *, payload: SuggestionCreatePayload):
        payload_dict = dict(payload)

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def list(self, *, knowledge_id: ObjectId):
        pipe = {'knowledge_id': knowledge_id}

        result = await self.collection.find(pipe).to_list(None)
        return [
            SuggestionRetrieve.model_validate(suggestion)
            for suggestion in result
        ]

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[SuggestionRetrieve, None]:
        result = await self.collection.find_one({by: value})

        return SuggestionRetrieve.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> SuggestionRetrieve:
        result = await self.collection.find_one({by: value})

        if result:
            return SuggestionRetrieve.model_validate(obj=result)

        raise SuggestionNotFound()
