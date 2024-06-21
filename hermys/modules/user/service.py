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
