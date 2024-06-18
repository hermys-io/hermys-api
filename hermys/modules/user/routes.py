from fastapi import APIRouter

from hermys.modules.user.dependencies import GetSharedUserService
from hermys.modules.user.schemas import UserCreatePayload

router = APIRouter()


@router.post('/')
async def create_user(
    payload: UserCreatePayload,
    shared_user_service: GetSharedUserService,
):
    result = await shared_user_service.create_and_send_confirmation_email(
        payload=payload,
    )

    return result.model_dump()
