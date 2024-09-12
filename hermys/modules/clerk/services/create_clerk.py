from typing import Annotated

from fastapi import Depends
from slugify import slugify

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
from hermys.modules.clerk.dependencies import GetClerkRepository
from hermys.modules.clerk.exceptions import ClerkAlreadyExists
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.schemas import (
    ClerkCreatePayload,
    ClerkDBO,
    ClerkRetrieve,
)
from hermys.modules.user.schemas import UserInternal
from hermys.settings import get_settings

settings = get_settings()


class CreateClerkService(ServiceABC[ClerkCreatePayload, ClerkRetrieve]):
    def __init__(
        self,
        clerk_repo: ClerkRepository,
        audit_service: AuditCreateService,
    ) -> None:
        self.clerk_repo = clerk_repo
        self.audit_service = audit_service

    async def perform(
        self,
        *,
        payload: ClerkCreatePayload,
    ):
        clerk_slug = slugify(payload.name)

        if await self.clerk_repo.exists(by='slug', value=clerk_slug):
            raise ClerkAlreadyExists()

        dbo = ClerkDBO(
            slug=clerk_slug,
            name=payload.name,
            description=payload.description,
            prompt=payload.prompt,
            gpt_model=payload.gpt_model,
            chat_title=payload.chat_title,
            active=True,
            photo_light=None,
            photo_dark=None,
            deleted_at=None,
        )

        result = await self.clerk_repo.create(dbo=dbo)

        return ClerkRetrieve.model_validate(result)

    async def audit(
        self,
        *,
        current_user: UserInternal,
        data: ClerkRetrieve,
    ):
        await self.audit_service.dispatch_non_blocking(
            payload=AuditCreatePayload(
                user_id=current_user.id,
                user_name=current_user.username,
                action=AuditActionEnum.CREATE,
                resource_id=data.id,
                resource_type=AuditResourceTypeEnum.CLERK,
                resource_readebly_name=data.name,
                status=AuditStatusEnum.SUCCESS,
            ),
            curren_user=current_user,
        )


def get_create_clerk_service(
    clerk_repo: GetClerkRepository,
    audit_service: GetAuditCreateService,
):
    return CreateClerkService(
        clerk_repo=clerk_repo,
        audit_service=audit_service,
    )


GetCreateClerkService = Annotated[
    CreateClerkService,
    Depends(get_create_clerk_service),
]
