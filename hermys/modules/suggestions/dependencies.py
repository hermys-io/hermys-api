from typing import Annotated

from fastapi import Depends

from hermys.db.db import GetDB
from hermys.modules.suggestions.repository import SuggestionRepository


def get_suggestion_repository(db: GetDB):
    return SuggestionRepository(db=db)


GetSuggestionRepository = Annotated[
    SuggestionRepository,
    Depends(get_suggestion_repository),
]
