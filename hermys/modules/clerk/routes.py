from typing import Literal

from fastapi import APIRouter, UploadFile, status

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.clerk.dependencies import GetClerkService
from hermys.modules.clerk.schemas import ClerkCreatePayload
from hermys.modules.clerk.services.create_clerk import GetCreateClerkService
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


# @with_permissions(roles=[UserRoleEnum.ADMIN])
@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_clerk(
    payload: ClerkCreatePayload,
    service: GetCreateClerkService,
    current_user: GetCurrentUser,
):
    result = await service.dispatch(current_user=current_user, payload=payload)

    return result.model_dump()


@router.post('/{clerk_id}/update-photo')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def update_photo(
    clerk_id: str,
    photo: UploadFile,
    clerk_service: GetClerkService,
    current_user: GetCurrentUser,
    _type: Literal['light', 'dark'] = 'light',
):
    result = await clerk_service.update_photo(
        current_user=current_user,
        clerk_id=clerk_id,
        photo=photo,
        _type=_type,
    )

    return result.model_dump()
