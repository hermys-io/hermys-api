from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from scout_apm.async_.starlette import ScoutMiddleware  # type: ignore

from hermys.db.shared_db import GetSharedDB
from hermys.integrations.scount_apm.config import configure_scout_apm
from hermys.modules.auth.exceptions import bind_auth_exceptions
from hermys.modules.auth.routes import router as auth_router
from hermys.modules.clerk.exceptions import bind_clerk_exceptions
from hermys.modules.clerk.routes import router as clerk_router
from hermys.modules.knowledge.exceptions import bind_knowledge_exceptions
from hermys.modules.knowledge.host_routes import (
    router as host_knowledge_router,
)
from hermys.modules.knowledge.routes import router as knowledge_router
from hermys.modules.organization.exceptions import bind_organization_exceptions
from hermys.modules.organization.routes import router as organization_router
from hermys.modules.suggestions.exceptions import bind_suggestion_exceptions
from hermys.modules.suggestions.routes import router as suggestion_router
from hermys.modules.user.exceptions import bind_user_exceptions
from hermys.modules.user.routes import router as user_router
from hermys.settings import get_settings

settings = get_settings()
configure_scout_apm()

app = FastAPI(
    title='Hermys API',
    default_response_class=ORJSONResponse,
)


# Middlewares
app.add_middleware(ScoutMiddleware)  # type: ignore
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
)
app.include_router(
    router=organization_router,
    prefix='/organization',
    tags=['organization'],
)
app.include_router(
    router=user_router,
    prefix='/user',
    tags=['user'],
)
app.include_router(
    router=clerk_router,
    prefix='/clerk',
    tags=['clerk'],
)
app.include_router(
    router=knowledge_router,
    prefix='/knowledge',
    tags=['knowledge'],
)
app.include_router(
    router=suggestion_router,
    prefix='/suggestion',
    tags=['suggestion'],
)
app.include_router(
    router=host_knowledge_router,
    prefix='/host-knowledge',
    tags=['host-knowledge'],
)


# Custom exceptions
bind_auth_exceptions(app)
bind_organization_exceptions(app)
bind_user_exceptions(app)
bind_clerk_exceptions(app)
bind_suggestion_exceptions(app)
bind_knowledge_exceptions(app)
