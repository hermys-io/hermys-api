from pydantic import BaseModel, ConfigDict, Field, field_validator

from hermys.db.base import ObjectIdField
from hermys.modules.auth.password import (
    get_hashed_password,
    is_password_strong,
)
from hermys.modules.user.enums import UserRoleEnum


class UserBase(BaseModel):
    username: str = Field(default=...)
    organization: str = Field(default=...)
    role: UserRoleEnum = Field(default=...)


class UserCreatePayload(UserBase):
    password: str = Field(default=...)

    @field_validator('password')
    def password_strength(cls, password: str):
        is_password_strong(password)

        return get_hashed_password(password)


class UserRetrieve(UserBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    active: bool = Field(default=...)

    model_config = ConfigDict(populate_by_name=True)


class UserInternal(UserRetrieve):
    password: str = Field(default=...)
