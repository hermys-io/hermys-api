from typing import Literal

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import UploadFile

from hermys.common.b2_helpers import get_clerk_filename
from hermys.integrations.b2.integration import B2Integration
from hermys.modules.clerk.exceptions import ClerkNotFound
from hermys.modules.clerk.repository import ClerkRepository
from hermys.modules.clerk.schemas import ClerkRetrieve, ClerkUpdatePayload
from hermys.modules.user.schemas import UserInternal


class ClerkService:
    def __init__(
        self,
        clerk_repo: ClerkRepository,
        b2_integration: B2Integration,
    ) -> None:
        self.clerk_repo = clerk_repo
        self.b2_integration = b2_integration

    async def update_photo(
        self,
        *,
        current_user: UserInternal,
        clerk_id: str,
        photo: UploadFile,
        _type: Literal['light', 'dark'],
    ) -> ClerkRetrieve:
        try:
            clerk_object_id = ObjectId(clerk_id)
        except InvalidId as exc:
            raise ClerkNotFound() from exc

        clerk = await self.clerk_repo.get_or_rise(
            by='_id',
            value=clerk_object_id,
        )

        if not photo.filename:
            raise Exception()

        file_name = get_clerk_filename(
            organization=current_user.organization,
            clerk_id=clerk_id,
            photo_name=photo.filename,
            _type=_type,
        )

        self.b2_integration.upload_file(photo, file_name=file_name)

        if _type == 'light':
            payload = ClerkUpdatePayload(photo_light=file_name)
        else:
            payload = ClerkUpdatePayload(photo_dark=file_name)

        result = await self.clerk_repo.update(
            clerk_id=ObjectId(clerk.id),
            payload=payload,
        )

        return ClerkRetrieve(**result.model_dump())
