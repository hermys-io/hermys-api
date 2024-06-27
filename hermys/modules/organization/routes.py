from fastapi import APIRouter

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.organization.dependencies import (
    GetSharedOrganizationService,
)
from hermys.modules.organization.schemas import OrganizationCreatePayload
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.post('/')
@with_permissions(roles=[UserRoleEnum.GOD])
async def create_organization(
    payload: OrganizationCreatePayload,
    shared_organization_service: GetSharedOrganizationService,
    _current_user: GetCurrentUser,
):
    result = await shared_organization_service.create(payload=payload)

    return result.model_dump()


@router.get('/')
@with_permissions(roles=[UserRoleEnum.GOD])
async def list_organizations(
    shared_organization_service: GetSharedOrganizationService,
    _current_user: GetCurrentUser,
):
    results = await shared_organization_service.list()

    return [result.model_dump() for result in results]
