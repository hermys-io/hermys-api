import pytest
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient

from hermys.db.dependencies import get_shared_db
from hermys.main import app
from hermys.settings import get_settings

settings = get_settings()


async def get_shared_db_override():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client['t-shared']

    try:
        yield db
    finally:
        collections = await db.list_collection_names()
        for collection in collections:
            await db.drop_collection(collection)

        client.close()


app.dependency_overrides[get_shared_db] = get_shared_db_override


@pytest.fixture()
async def client():
    return TestClient(app)


@pytest.fixture()
async def shared_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client['t-shared']

    try:
        yield db
    finally:
        collections = await db.list_collection_names()
        for collection in collections:
            await db.drop_collection(collection)

        client.close()


@pytest.fixture
def anyio_backend():
    return 'asyncio'
