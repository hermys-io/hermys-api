from typing import List

from hermys.modules.organization.repository import OrganizationRepository
from hermys.modules.organization.schemas import (
    OrganizationCreatePayload,
    OrganizationRetrieve,
)


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepository) -> None:
        self.organization_repo = organization_repo

    async def create(
        self,
        *,
        payload: OrganizationCreatePayload,
    ) -> OrganizationRetrieve:
        created_organization = await self.organization_repo.create(
            payload=payload,
        )
        return OrganizationRetrieve(**created_organization.model_dump())

    async def list(self) -> List[OrganizationRetrieve]:
        results = await self.organization_repo.list()
        return results
