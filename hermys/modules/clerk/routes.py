from fastapi import APIRouter

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.clerk.dependencies import GetClerkService
from hermys.modules.clerk.schemas import ClerkCreatePayload
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.post('/')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def create_clerk(
    payload: ClerkCreatePayload,
    clerk_service: GetClerkService,
    _current_user: GetCurrentUser,
):
    result = await clerk_service.create(payload=payload)

    return result.model_dump()
