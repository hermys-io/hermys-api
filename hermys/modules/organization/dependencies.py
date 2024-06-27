from typing import Annotated

from fastapi import Depends

from hermys.db.dependencies import GetSharedDB
from hermys.modules.organization.repository import OrganizationRepository
from hermys.modules.organization.service import OrganizationService


def get_shared_organization_repository(shared_db: GetSharedDB):
    return OrganizationRepository(db=shared_db)


GetSharedOrganizationRepository = Annotated[
    OrganizationRepository,
    Depends(get_shared_organization_repository),
]


def get_shared_organization_service(
    shared_organization_repo: GetSharedOrganizationRepository,
):
    return OrganizationService(organization_repo=shared_organization_repo)


GetSharedOrganizationService = Annotated[
    OrganizationService,
    Depends(get_shared_organization_service),
]
