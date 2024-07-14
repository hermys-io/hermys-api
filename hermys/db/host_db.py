from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from hermys.common.host_name_dependencies import GetHostName
from hermys.db.config import get_db_config
from hermys.modules.organization.dependencies import (
    GetSharedOrganizationService,
)


async def get_host_db(
    organization_service: GetSharedOrganizationService,
    host_name: GetHostName,
):
    organization = await organization_service.retrieve_or_rise(
        by='host',
        value=host_name,
    )

    tenant_name = f'org-{organization.name}'
    client, db = get_db_config(db_name=tenant_name)

    try:
        yield db
    finally:
        client.close()


GetHostDB = Annotated[
    AsyncIOMotorDatabase,
    Depends(get_host_db),
]
