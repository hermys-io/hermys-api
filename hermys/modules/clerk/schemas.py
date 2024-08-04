from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField
from hermys.modules.clerk.enums import OpenAiGPTModelEnum


class ClerkBase(BaseModel):
    name: str = Field(default=...)
    description: Optional[str] = Field(default=...)
    prompt: str = Field(default=...)
    gpt_model: OpenAiGPTModelEnum = Field(
        default=OpenAiGPTModelEnum.GPT_4o_MINI,
    )


class ClerkCreatePayload(ClerkBase):
    ...


class ClerkRetrieve(ClerkBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    active: bool = Field(default=...)
    slug: str = Field(default=...)
    photo_light: Optional[str] = Field(default=None)
    photo_dark: Optional[str] = Field(default=None)

    model_config = ConfigDict(populate_by_name=True)


class ClerkUpdatePayload(BaseModel):
    photo_light: Optional[str] = Field(default=None)
    photo_dark: Optional[str] = Field(default=None)
