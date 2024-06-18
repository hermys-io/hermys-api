from fastapi.routing import APIRouter

from hermys.modules.auth.dependencies import GetAuthService
from hermys.modules.auth.schemas import LoginCredentialPayload

router = APIRouter()


@router.post('/token')
async def get_token(
    login_credentials: LoginCredentialPayload,
    auth_service: GetAuthService,
):
    access_token = await auth_service.get_token(
        login_credentials=login_credentials,
    )
    return {'access_token': access_token}
