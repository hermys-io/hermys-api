from fastapi import APIRouter, status

from hermys.modules.auth.dependencies import GetCurrentUser
from hermys.modules.auth.permissions import with_permissions
from hermys.modules.user.dependencies import GetSharedUserService
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.schemas import UserCreatePayload, UserRetrieve

router = APIRouter()


@router.get('/me', status_code=status.HTTP_200_OK)
async def get_current_authenticated_user(current_user: GetCurrentUser):
    return UserRetrieve.model_validate(current_user.model_dump()).model_dump()


@router.post('/', status_code=status.HTTP_201_CREATED)
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def create_user(
    payload: UserCreatePayload,
    shared_user_service: GetSharedUserService,
    _current_user: GetCurrentUser,
):
    result = await shared_user_service.create(
        payload=payload,
    )

    return result.model_dump()


@router.get('/')
@with_permissions(roles=[UserRoleEnum.ADMIN])
async def list_users(
    shared_user_service: GetSharedUserService,
    current_user: GetCurrentUser,
):
    results = await shared_user_service.list(
        organization=current_user.organization,
    )

    return [result.model_dump() for result in results]


@router.get('/{user_id}')
@with_permissions(roles=[UserRoleEnum.ADMIN, UserRoleEnum.USER])
async def retrieve_user(
    user_id: str,
    shared_user_service: GetSharedUserService,
    _current_user: GetCurrentUser,
):
    result = await shared_user_service.retrieve(user_id=user_id)

    return result.model_dump()
