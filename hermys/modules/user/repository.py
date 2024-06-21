from typing import Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.exceptions import UserAlreadyExists, UserNotFound
from hermys.modules.user.schemas import UserCreatePayload, UserInternal


class UserRepository:
    collection_name = 'users'

    def __init__(self, *, db: AsyncIOMotorDatabase) -> None:
        self.collection = db[self.collection_name]

    async def create(self, *, payload: UserCreatePayload) -> UserInternal:
        if await self.get(by='username', value=payload.username):
            raise UserAlreadyExists()

        payload_dict = payload.model_dump()
        payload_dict['active'] = False

        result = await self.collection.insert_one(payload_dict)
        return await self.get_or_rise(by='_id', value=result.inserted_id)

    async def list(self, *, organization: str):
        default_filter = {
            'organization': organization,
            'role': {'$ne': UserRoleEnum.GOD},
        }
        results = await self.collection.find(default_filter).to_list(None)
        return [UserInternal.model_validate(result) for result in results]

    async def get(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> Union[UserInternal, None]:
        result = await self.collection.find_one({by: value})

        return UserInternal.model_validate(result) if result else None

    async def get_or_rise(
        self,
        *,
        by: str,
        value: Union[str, ObjectId],
    ) -> UserInternal:
        result = await self.collection.find_one({by: value})

        if result:
            return UserInternal.model_validate(obj=result)

        raise UserNotFound()
