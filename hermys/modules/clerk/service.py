from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.schemas import ClerkCreatePayload, ClerkRetrieve


class ClerkService:
    def __init__(self, clerk_repo: ClerkRepository) -> None:
        self.clerk_repo = clerk_repo

    async def create(
        self,
        *,
        payload: ClerkCreatePayload,
    ) -> ClerkRetrieve:
        created_clerk = await self.clerk_repo.create(
            payload=payload,
        )
        return ClerkRetrieve(**created_clerk.model_dump())
