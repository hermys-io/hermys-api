from fastapi import APIRouter

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.user.dependencies import GetSharedUserService
from hermys.modules.user.schemas import UserCreatePayload, UserRetrieve

router = APIRouter()


@router.get("/me")
async def get_current_authenticated_user(current_user: GetCurrentUser):
    return UserRetrieve.model_validate(current_user.model_dump()).model_dump()


@router.post("/")
async def create_user(
    payload: UserCreatePayload,
    shared_user_service: GetSharedUserService,
):
    result = await shared_user_service.create_and_send_confirmation_email(
        payload=payload,
    )

    return result.model_dump()
