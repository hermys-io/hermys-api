from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField
from hermys.modules.clerk.enums import OpenAiGPTModelEnum


class ClerkDBO(BaseModel):
    id: ObjectIdField = Field(default=None, alias='_id')
    slug: str = Field(default=...)
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    prompt: str = Field(default=...)
    gpt_model: OpenAiGPTModelEnum = Field(
        default=OpenAiGPTModelEnum.GPT_4o_MINI,
    )
    chat_title: str = Field(default=...)
    photo_light: Optional[str] = Field(default=None)
    photo_dark: Optional[str] = Field(default=None)
    active: bool = Field(default=True)
    deleted_at: Optional[datetime] = Field(default=None)

    model_config = ConfigDict(populate_by_name=True)


class ClerkCreatePayload(BaseModel):
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    prompt: str = Field(default=...)
    gpt_model: OpenAiGPTModelEnum = Field(
        default=OpenAiGPTModelEnum.GPT_4o_MINI,
    )
    chat_title: str = Field(default=...)


class ClerkRetrieve(BaseModel):
    id: ObjectIdField = Field(default=..., alias='_id')
    slug: str = Field(default=...)
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    chat_title: str = Field(default=...)
    photo_light: Optional[str] = Field(default=None)
    photo_dark: Optional[str] = Field(default=None)
    active: bool = Field(default=True)

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class ClerkUpdatePayload(BaseModel):
    photo_light: Optional[str] = Field(default=None)
    photo_dark: Optional[str] = Field(default=None)
