from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField


class SuggestionBase(BaseModel):
    text: str = Field(default=...)
    source: ObjectIdField = Field(default=...)
    active: bool = Field(default=True)


class SuggestionCreatePayload(SuggestionBase):
    pass


class SuggestionRetrieve(SuggestionBase):
    id: ObjectIdField = Field(default=..., alias='_id')

    model_config = ConfigDict(populate_by_name=True)
