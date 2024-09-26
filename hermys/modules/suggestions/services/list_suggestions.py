from typing import Annotated

from bson import ObjectId
from fastapi import Depends

from hermys.db.base import ObjectIdField
from hermys.modules.suggestions.dependencies import GetSuggestionRepository
from hermys.modules.suggestions.repository import SuggestionRepository
from hermys.settings import get_settings

settings = get_settings()


class ListSuggestionService:
    def __init__(
        self,
        suggestion_repo: SuggestionRepository,
    ) -> None:
        self.suggestion_repo = suggestion_repo

    async def dispatch(self, *, knowledge_id: ObjectIdField):
        suggestions = await self.suggestion_repo.list(
            knowledge_id=ObjectId(knowledge_id)
        )
        return suggestions


def get_list_suggestion_service(suggestion_repo: GetSuggestionRepository):
    return ListSuggestionService(suggestion_repo=suggestion_repo)


GetListSuggestionService = Annotated[
    ListSuggestionService,
    Depends(get_list_suggestion_service),
]
