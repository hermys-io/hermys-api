from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.schemas import KnowledgeCreatePayload


class KnowledgeService:
    def __init__(self, knowledge_repo: KnowledgeRepository):
        self.knowledge_repo = knowledge_repo

    async def create(self, *, payload: KnowledgeCreatePayload):
        result = await self.knowledge_repo.create(payload=payload)
        return result
