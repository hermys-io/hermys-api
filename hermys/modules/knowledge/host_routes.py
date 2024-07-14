from fastapi import APIRouter

from hermys.modules.knowledge.dependencies import GetHostKnowledgeService

router = APIRouter()


@router.get('/', status_code=200)
async def list_knowledge(
    clerk_slug: str,
    knowledge_service: GetHostKnowledgeService,
):
    results = await knowledge_service.list(clerk_slug=clerk_slug)

    return [result.model_dump() for result in results]
