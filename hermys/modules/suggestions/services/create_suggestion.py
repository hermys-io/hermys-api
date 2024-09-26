from typing import Annotated

from bson import ObjectId
from fastapi import Depends

from hermys.common.abstract_service import ServiceABC
from hermys.modules.audit.enums import (
    AuditActionEnum,
    AuditResourceTypeEnum,
    AuditStatusEnum,
)
from hermys.modules.audit.schemas import AuditCreatePayload
from hermys.modules.audit.services import (
    AuditCreateService,
    GetAuditCreateService,
)
from hermys.modules.knowledge.dependencies import GetKnowledgeRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.suggestions.dependencies import GetSuggestionRepository
from hermys.modules.suggestions.repository import SuggestionRepository
from hermys.modules.suggestions.schemas import (
    SuggestionCreatePayload,
    SuggestionRetrieve,
)
from hermys.modules.user.schemas import UserInternal
from hermys.settings import get_settings

settings = get_settings()


class CreateSuggestionService(
    ServiceABC[SuggestionCreatePayload, SuggestionRetrieve],
):
    def __init__(
        self,
        suggestion_repo: SuggestionRepository,
        knowledge_repo: KnowledgeRepository,
        audit_service: AuditCreateService,
    ) -> None:
        self.suggestion_repo = suggestion_repo
        self.knowledge_repo = knowledge_repo
        self.audit_service = audit_service

    async def perform(
        self,
        *,
        payload: SuggestionCreatePayload,
    ):
        await self.knowledge_repo.get_or_rise(
            by='_id',
            value=ObjectId(payload.knowledge_id),
        )

        created_suggestion = await self.suggestion_repo.create(payload=payload)
        return created_suggestion

    async def audit(
        self,
        *,
        current_user: UserInternal,
        data: SuggestionRetrieve,
    ):
        await self.audit_service.dispatch_non_blocking(
            payload=AuditCreatePayload(
                user_id=current_user.id,
                user_name=current_user.username,
                action=AuditActionEnum.CREATE,
                resource_id=data.id,
                resource_type=AuditResourceTypeEnum.SUGGESTION,
                resource_readebly_name=data.text,
                status=AuditStatusEnum.SUCCESS,
            ),
            curren_user=current_user,
        )


def get_create_suggestion_service(
    suggestion_repo: GetSuggestionRepository,
    knowledge_repo: GetKnowledgeRepository,
    audit_service: GetAuditCreateService,
):
    return CreateSuggestionService(
        suggestion_repo=suggestion_repo,
        knowledge_repo=knowledge_repo,
        audit_service=audit_service,
    )


GetCreateSuggestionService = Annotated[
    CreateSuggestionService,
    Depends(get_create_suggestion_service),
]
