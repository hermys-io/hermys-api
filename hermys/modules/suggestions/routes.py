from fastapi import APIRouter

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.suggestions.dependencies import GetSuggestionRepository
from hermys.modules.suggestions.schemas import SuggestionCreatePayload
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.post('/')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def create_suggestion(
    payload: SuggestionCreatePayload,
    repo: GetSuggestionRepository,
    _current_user: GetCurrentUser,
):
    await repo.create(payload=payload)
    return None
