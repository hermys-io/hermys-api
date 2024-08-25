from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel

from hermys.modules.user.schemas import UserInternal

CreatePayloadType = TypeVar('CreatePayloadType', bound=BaseModel)
RetrieveType = TypeVar('RetrieveType', bound=BaseModel)


class ServiceABC(ABC, Generic[CreatePayloadType, RetrieveType]):
    async def dispatch(
        self,
        *,
        current_user: UserInternal,
        payload: CreatePayloadType,
    ) -> RetrieveType:
        result = await self.perform(payload=payload)
        await self.audit(current_user=current_user, data=result)

        return result

    @abstractmethod
    async def perform(
        self,
        *,
        payload: CreatePayloadType,
    ) -> RetrieveType:
        raise NotImplementedError()

    @abstractmethod
    async def audit(
        self,
        *,
        current_user: UserInternal,
        data: RetrieveType,
    ) -> None:
        raise NotImplementedError()
