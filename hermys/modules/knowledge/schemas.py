from pydantic import BaseModel, Field

from hermys.db.base import ObjectIdField


class KnowledgeBase(BaseModel):
    name: str = Field(default=...)
    alt_text: str = Field(default=...)
    clerk: ObjectIdField = Field(default=...)
    chunk_size: int = Field(default=500)
    chunk_overlap: int = Field(default=200)
    top_k: int = Field(default=5)


class KnowledgeCreatePayload(KnowledgeBase):
    pass


class KnowledgeRetrieve(KnowledgeBase):
    pass
