from fastapi import APIRouter

from hermys.integrations.b2.dependencies import GetB2Integration
from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.get('/get-signed-image')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def get_signed_image(
    b2_integration: GetB2Integration,
    filename: str,
    _current_user: GetCurrentUser,
    valid_duration_in_seconds: int = 3600,
):
    result = b2_integration.get_file(
        filename=filename,
        valid_duration_in_seconds=valid_duration_in_seconds,
    )
    return result
