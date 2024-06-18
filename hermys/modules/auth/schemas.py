from pydantic import BaseModel

from hermys.db.base import ObjectIdField


class LoginCredentialPayload(BaseModel):
    username: str
    password: str


class AccessTokenData(BaseModel):
    id: ObjectIdField
    username: str
    role: str
    organization: str
    active: bool
