from typing import Annotated

from bson import ObjectId
from fastapi import Depends, UploadFile

from hermys.common.b2_helpers import get_knowledge_filename
from hermys.db.base import ObjectIdField
from hermys.integrations.b2.dependencies import GetB2Integration
from hermys.integrations.b2.integration import B2Integration
from hermys.modules.knowledge.dependencies import GetKnowledgeRepository
from hermys.modules.knowledge.respository import KnowledgeRepository
from hermys.modules.knowledge.schemas import KnowledgeUpdatePayload
from hermys.settings import get_settings

settings = get_settings()


class KnowledgeAddPhotoService:
    def __init__(
        self,
        knowledge_repo: KnowledgeRepository,
        b2_integration: B2Integration,
    ) -> None:
        self.knowledge_repo = knowledge_repo
        self.b2_integration = b2_integration

    async def dispatch(
        self,
        knowledge_id: ObjectIdField,
        organization: str,
        photo: UploadFile,
    ):
        await self.knowledge_repo.get_or_rise(
            by='_id',
            value=ObjectId(knowledge_id),
        )

        if not photo.filename:
            # TODO: Create a custom exception
            raise Exception()

        file_name = get_knowledge_filename(
            organization=organization,
            knowledge_id=knowledge_id,
            photo_name=photo.filename,
        )

        self.b2_integration.upload_file(photo, file_name=file_name)

        payload = KnowledgeUpdatePayload(photo=file_name)
        result = await self.knowledge_repo.update(
            clerk_id=ObjectId(knowledge_id),
            payload=payload,
        )

        return result


def get_knowledge_add_photo_service(
    knowledge_repo: GetKnowledgeRepository,
    b2_integration: GetB2Integration,
):
    return KnowledgeAddPhotoService(
        knowledge_repo=knowledge_repo,
        b2_integration=b2_integration,
    )


GetKnowledgeAddPhotoService = Annotated[
    KnowledgeAddPhotoService,
    Depends(get_knowledge_add_photo_service),
]
