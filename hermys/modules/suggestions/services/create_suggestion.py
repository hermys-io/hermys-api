from typing import Annotated

from bson import ObjectId
from fastapi import Depends

from hermys.modules.knowledge.dependencies import GetKnowledgeRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.suggestions.dependencies import GetSuggestionRepository
from hermys.modules.suggestions.repository import SuggestionRepository
from hermys.modules.suggestions.schemas import SuggestionCreatePayload
from hermys.settings import get_settings

settings = get_settings()


class CreateSuggestionService:
    def __init__(
        self,
        suggestion_repo: SuggestionRepository,
        knowledge_repo: KnowledgeRepository,
    ) -> None:
        self.suggestion_repo = suggestion_repo
        self.knowledge_repo = knowledge_repo

    async def dispatch(self, *, payload: SuggestionCreatePayload):
        await self.knowledge_repo.get_or_rise(
            by='_id',
            value=ObjectId(payload.knowledge_id),
        )

        created_suggestion = await self.suggestion_repo.create(payload=payload)
        return created_suggestion


def get_create_suggestion_service(
    suggestion_repo: GetSuggestionRepository,
    knowledge_repo: GetKnowledgeRepository,
):
    return CreateSuggestionService(
        suggestion_repo=suggestion_repo,
        knowledge_repo=knowledge_repo,
    )


GetCreateSuggestionService = Annotated[
    CreateSuggestionService,
    Depends(get_create_suggestion_service),
]
