from typing import Annotated

from fastapi import Depends

from hermys.db.db import GetDB
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.service import KnowledgeService


def get_knowledge_repository(db: GetDB):
    return KnowledgeRepository(db=db)


GetKnowledgeRepository = Annotated[
    KnowledgeRepository,
    Depends(get_knowledge_repository),
]


def get_knowledge_service(knowledge_repo: GetKnowledgeRepository):
    return KnowledgeService(knowledge_repo=knowledge_repo)


GetKnowledgeService = Annotated[
    KnowledgeService,
    Depends(get_knowledge_service),
]
