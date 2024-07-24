from fastapi import APIRouter, UploadFile

from hermys.db.base import ObjectIdField
from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.knowledge.dependencies import GetKnowledgeService
from hermys.modules.knowledge.schemas import KnowledgeCreatePayload
from hermys.modules.knowledge.services import (
    GetKnowledgeAddPhotoService,
    GetKnowledgeTrainService,
)
from hermys.modules.user.enums import UserRoleEnum

router = APIRouter()


@router.post('/')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def create_knowledge(
    payload: KnowledgeCreatePayload,
    knowledge_service: GetKnowledgeService,
    _current_user: GetCurrentUser,
):
    result = await knowledge_service.create(payload=payload)
    return result.model_dump()


@router.post('/{knowledge_id}/add-photo')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def add_photo(
    knowledge_id: ObjectIdField,
    photo: UploadFile,
    knowledge_add_photo_service: GetKnowledgeAddPhotoService,
    current_user: GetCurrentUser,
):
    result = await knowledge_add_photo_service.dispatch(
        knowledge_id=knowledge_id,
        organization=current_user.organization,
        photo=photo,
    )

    return result.model_dump()


@router.post('/{knowledge_id}/train')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def train_knowledge(
    knowledge_id: ObjectIdField,
    knowledge_train_service: GetKnowledgeTrainService,
    current_user: GetCurrentUser,
):
    await knowledge_train_service.dispatch(
        knowledge_id=str(knowledge_id),
        index_name=current_user.organization,
    )

    return None
