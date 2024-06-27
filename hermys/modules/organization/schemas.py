from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField


class OrganizationBase(BaseModel):
    name: str = Field(default=...)
    display_name: str = Field(default=...)
    host: str = Field(default=...)


class OrganizationCreatePayload(OrganizationBase):
    ...


class OrganizationRetrieve(OrganizationBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    active: bool = Field(default=...)

    model_config = ConfigDict(populate_by_name=True)
