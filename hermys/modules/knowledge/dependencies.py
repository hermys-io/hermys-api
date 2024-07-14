from typing import Annotated

from fastapi import Depends

from hermys.db.db import GetDB
from hermys.db.host_db import GetHostDB
from hermys.modules.clerk.dependencies import GetClerkRepository
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.service import KnowledgeService


def get_knowledge_repository(db: GetDB):
    return KnowledgeRepository(db=db)


GetKnowledgeRepository = Annotated[
    KnowledgeRepository,
    Depends(get_knowledge_repository),
]


def get_knowledge_service(
    knowledge_repo: GetKnowledgeRepository, clerk_repo: GetClerkRepository
):
    return KnowledgeService(
        knowledge_repo=knowledge_repo,
        clerk_repo=clerk_repo,
    )


GetKnowledgeService = Annotated[
    KnowledgeService,
    Depends(get_knowledge_service),
]


def get_host_knowledge_repository(host_db: GetHostDB):
    return KnowledgeRepository(db=host_db)


GetHostKnowledgeRepository = Annotated[
    KnowledgeRepository,
    Depends(get_host_knowledge_repository),
]


def get_host_knowledge_service(
    host_knowledge_repo: GetHostKnowledgeRepository,
    host_db: GetHostDB,
):
    clerk_repo = ClerkRepository(db=host_db)
    return KnowledgeService(
        knowledge_repo=host_knowledge_repo,
        clerk_repo=clerk_repo,
    )


GetHostKnowledgeService = Annotated[
    KnowledgeService,
    Depends(get_host_knowledge_service),
]
