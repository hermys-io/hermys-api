import asyncio
from typing import Annotated, Union

from bson import ObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.db.config import get_db_config
from hermys.db.db import GetDB
from hermys.modules.audit.exceptions import AuditNotFound
from hermys.modules.audit.schemas import AuditCreatePayload, AuditInternal
from hermys.modules.user.schemas import UserInternal


class AuditRepository:
    collection_name = 'audit'

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[self.collection_name]

    async def create(self, *, payload: AuditCreatePayload):
        payload_dict = dict(payload)

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def create_non_blocking(
        self,
        *,
        payload: AuditCreatePayload,
        curren_user: UserInternal,
    ):
        client, db = get_db_config(db_name=f'org-{curren_user.organization}')

        await asyncio.sleep(50)
        collection = db[self.collection_name]
        payload_dict = dict(payload)
        result = await collection.insert_one(payload_dict)

        client.close()
        return result

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[AuditInternal, None]:
        result = await self.collection.find_one({by: value})

        return AuditInternal.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> AuditInternal:
        result = await self.collection.find_one({by: value})

        if result:
            return AuditInternal.model_validate(result)

        raise AuditNotFound()


def get_audit_repository(db: GetDB):
    return AuditRepository(db=db)


GetAuditRepository = Annotated[
    AuditRepository,
    Depends(get_audit_repository),
]
