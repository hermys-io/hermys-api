from pydantic import BaseModel, ConfigDict, Field

from hermys.db.base import ObjectIdField


class SuggestionBase(BaseModel):
    text: str = Field(default=...)
    active: bool = Field(default=True)
    knowledge_id: ObjectIdField = Field(default=...)


class SuggestionCreatePayload(SuggestionBase):
    pass


class SuggestionRetrieve(SuggestionBase):
    id: ObjectIdField = Field(default=..., alias='_id')

    model_config = ConfigDict(populate_by_name=True)
