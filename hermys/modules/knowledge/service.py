from bson import ObjectId

from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.schemas import KnowledgeCreatePayload


class KnowledgeService:
    def __init__(
        self,
        knowledge_repo: KnowledgeRepository,
        clerk_repo: ClerkRepository,
    ):
        self.knowledge_repo = knowledge_repo
        self.clerk_repo = clerk_repo

    async def create(self, *, payload: KnowledgeCreatePayload):
        result = await self.knowledge_repo.create(payload=payload)
        return result

    async def list(self, *, clerk_slug: str):
        clerk = await self.clerk_repo.get_or_rise(by='slug', value=clerk_slug)
        result = await self.knowledge_repo.list(clerk_id=ObjectId(clerk.id))
        return result
