from motor.motor_asyncio import AsyncIOMotorClient

from hermys.settings import get_settings

settings = get_settings()


def get_db_config(*, db_name: str = 'shared'):
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[db_name]

    return client, db
