from fastapi import APIRouter

from hermys.db.base import ObjectIdField
from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.suggestions.schemas import SuggestionCreatePayload
from hermys.modules.suggestions.services import (
    GetCreateSuggestionService,
    GetListSuggestionService,
)
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.post('/')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def create_suggestion(
    payload: SuggestionCreatePayload,
    service: GetCreateSuggestionService,
    current_user: GetCurrentUser,
):
    result = await service.dispatch(current_user=current_user, payload=payload)

    return result.model_dump()


@router.get('/')
@with_permissions(roles=[UserRoleEnum.ADMIN, UserRoleEnum.USER])
async def list_suggestions(
    knowledge_id: ObjectIdField,
    service: GetListSuggestionService,
    _current_user: GetCurrentUser,
):
    result = await service.dispatch(knowledge_id=knowledge_id)
    return [suggestion.model_dump() for suggestion in result]
