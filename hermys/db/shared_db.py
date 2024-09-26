from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.db.config import get_db_config


async def get_shared_db():
    client, db = get_db_config(db_name='shared')

    try:
        yield db
    finally:
        client.close()


GetSharedDB = Annotated[
    AsyncIOMotorDatabase,
    Depends(get_shared_db),
]
