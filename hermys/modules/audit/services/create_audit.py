from typing import Annotated

from fastapi import BackgroundTasks, Depends

from hermys.modules.audit.repository import AuditRepository, GetAuditRepository
from hermys.modules.audit.schemas import AuditCreatePayload
from hermys.modules.user.schemas import UserInternal


class AuditCreateService:
    def __init__(
        self,
        audit_repo: AuditRepository,
        background_tasks: BackgroundTasks,
    ):
        self.audit_repo = audit_repo
        self.background_tasks = background_tasks

    async def dispatch_non_blocking(
        self,
        *,
        payload: AuditCreatePayload,
        curren_user: UserInternal,
    ):
        self.background_tasks.add_task(
            self.audit_repo.create_non_blocking,
            payload=payload,
            curren_user=curren_user,
        )


def get_audit_create_service(
    audit_repo: GetAuditRepository,
    background_tasks: BackgroundTasks,
):
    return AuditCreateService(
        audit_repo=audit_repo,
        background_tasks=background_tasks,
    )


GetAuditCreateService = Annotated[
    AuditCreateService,
    Depends(get_audit_create_service),
]
