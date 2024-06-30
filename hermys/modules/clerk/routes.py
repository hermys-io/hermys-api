from fastapi import APIRouter, UploadFile

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


@router.post('/{clerk_id}/update-photo')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def update_photo(
    clerk_id: str,
    photo: UploadFile,
    clerk_service: GetClerkService,
    current_user: GetCurrentUser,
):
    result = await clerk_service.update_photo(
        current_user=current_user,
        clerk_id=clerk_id,
        photo=photo,
    )

    return result.model_dump()
