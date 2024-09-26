from typing import List, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.organization.exceptions import (
    OrganizationAlreadyExists,
    OrganizationNotFound,
)
from hermys.modules.organization.schemas import (
    OrganizationCreatePayload,
    OrganizationRetrieve,
)


class OrganizationRepository:
    collection_name = 'organization'

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[self.collection_name]

    async def create(
        self,
        *,
        payload: OrganizationCreatePayload,
    ) -> OrganizationRetrieve:
        if await self.get(by='name', value=payload.name):
            raise OrganizationAlreadyExists()

        payload_dict = payload.model_dump()
        payload_dict['active'] = False

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def list(self) -> List[OrganizationRetrieve]:
        results = await self.collection.find({}).to_list(None)
        return [
            OrganizationRetrieve.model_validate(result) for result in results
        ]

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[OrganizationRetrieve, None]:
        result = await self.collection.find_one({by: value})

        return OrganizationRetrieve.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> OrganizationRetrieve:
        result = await self.collection.find_one({by: value})

        if result:
            return OrganizationRetrieve.model_validate(obj=result)

        raise OrganizationNotFound()
