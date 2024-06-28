from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.db.config import get_db_config
from hermys.modules.auth.dependencies import GetCurrentUser


async def get_db(curren_user: GetCurrentUser):
    client, db = get_db_config(db_name=f'org-{curren_user.organization}')

    try:
        yield db
    finally:
        client.close()


GetDB = Annotated[
    AsyncIOMotorDatabase,
    Depends(get_db),
]
