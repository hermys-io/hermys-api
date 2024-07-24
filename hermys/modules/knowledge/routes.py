from fastapi import APIRouter

from hermys.db.base import ObjectIdField
from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.knowledge.dependencies import GetKnowledgeService
from hermys.modules.knowledge.schemas import KnowledgeCreatePayload
from hermys.modules.knowledge.services.train_knowledge import (
    GetTrainKnowledgeService,
)

router = APIRouter()


@router.post('/')
async def create_knowledge(
    payload: KnowledgeCreatePayload,
    knowledge_service: GetKnowledgeService,
    _current_user: GetCurrentUser,
):
    result = await knowledge_service.create(payload=payload)
    return result.model_dump()


@router.post('/{knowledge_id}/train')
async def train_knowledge(
    knowledge_id: ObjectIdField,
    train_knowledge_service: GetTrainKnowledgeService,
    current_user: GetCurrentUser,
):
    await train_knowledge_service.dispatch(
        knowledge_id=str(knowledge_id),
        index_name=current_user.organization,
    )

    return None
