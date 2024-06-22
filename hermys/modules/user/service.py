from bson import ObjectId

from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.exceptions import UserNotFound
from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload, UserRetrieve


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def create(
        self,
        *,
        payload: UserCreatePayload,
    ) -> UserRetrieve:
        created_user = await self.user_repo.create(payload=payload)
        return UserRetrieve(**created_user.model_dump())

    async def list(self, *, organization: str):
        results = await self.user_repo.list(organization=organization)
        return [UserRetrieve(**result.model_dump()) for result in results]

    async def retrieve(self, *, user_id: str):
        if not ObjectId.is_valid(user_id):
            raise UserNotFound()

        user = await self.user_repo.get_or_rise(
            by='_id',
            value=ObjectId(user_id),
        )

        if user.role == UserRoleEnum.GOD:
            raise UserNotFound()

        return UserRetrieve(**user.model_dump())
