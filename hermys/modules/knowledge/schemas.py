from typing import Optional

from pydantic import BaseModel, Field

from hermys.db.base import ObjectIdField


class KnowledgeBase(BaseModel):
    pdf_url: str = Field(default=...)
    name: str = Field(default=...)
    alt_text: str = Field(default=...)
    clerk: ObjectIdField = Field(default=...)
    active: bool = Field(default=...)
    chunk_size: int = Field(default=500)
    chunk_overlap: int = Field(default=200)
    top_k: int = Field(default=5)
    prompt_copmlement: str = Field(default='')
    welcome_message: str = Field(default='')


class KnowledgeCreatePayload(KnowledgeBase):
    pass


class KnowledgeRetrieve(KnowledgeBase):
    id: ObjectIdField = Field(default=..., alias='_id')
    photo: Optional[str] = Field(default=None)


class KnowledgeUpdatePayload(BaseModel):
    photo: Optional[str] = Field(default=None)
