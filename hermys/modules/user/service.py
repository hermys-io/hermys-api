from hermys.modules.user.repository import UserRepository
from hermys.modules.user.schemas import UserCreatePayload, UserRetrieve


class UserService:
    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    async def create_and_send_confirmation_email(
        self,
        *,
        payload: UserCreatePayload,
    ) -> UserRetrieve:
        return await self.user_repo.create(payload=payload)
