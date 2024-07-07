from fastapi import APIRouter

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.knowledge.dependencies import GetKnowledgeService
from hermys.modules.knowledge.schemas import KnowledgeCreatePayload

router = APIRouter()


@router.post('/')
async def create_knowledge(
    payload: KnowledgeCreatePayload,
    knowledge_service: GetKnowledgeService,
    _current_user: GetCurrentUser,
):
    result = await knowledge_service.create(payload=payload)
    return result.model_dump()
