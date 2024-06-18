from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from scout_apm.api import Config  # type: ignore
from scout_apm.async_.starlette import ScoutMiddleware  # type: ignore

from hermys.db.dependencies import GetSharedDB
from hermys.modules.auth.exceptions import bind_auth_exceptions
from hermys.modules.auth.routes import router as auth_router
from hermys.modules.user.exceptions import bind_user_exceptions
from hermys.modules.user.routes import router as user_router
from hermys.settings import get_settings

settings = get_settings()
Config.set(
    key='504d3050ee266f4f3be0f129f1fdfa43',
    name='Hermys API - FastAPI',
    monitor=True,
)

app = FastAPI(title='Hermys API')

app.add_middleware(ScoutMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(','),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health', tags=['health'])
async def health(db: GetSharedDB):
    try:
        await db.client.server_info()
        db_status = 'up'
    except Exception:
        db_status = 'down'

    return {'api': 'up', 'db': db_status}


# Routes
app.include_router(
    router=auth_router,
    prefix='/auth',
    tags=['auth'],
    default_response_class=ORJSONResponse,
)
app.include_router(
    router=user_router,
    prefix='/users',
    tags=['users'],
    default_response_class=ORJSONResponse,
)

# Custom exceptions
bind_auth_exceptions(app)
bind_user_exceptions(app)
