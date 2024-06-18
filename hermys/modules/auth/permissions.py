from functools import wraps
from typing import Any, Callable, TypeVar

from fastapi import FastAPI

from hermys.modules.auth.exceptions import DoesNotHavePermission
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.schemas import UserInternal

F = TypeVar('F', bound=Callable[..., Any])


app = FastAPI()


def with_permissions(roles: str) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            user: UserInternal | None = kwargs.get('current_user')

            if not user:
                raise EnvironmentError('Current online user was not provided')

            if user.role == UserRoleEnum.ADMIN or user.role in roles:
                result = await func(*args, **kwargs)
                return result

            raise DoesNotHavePermission()

        return wrapper  # type: ignore

    return decorator
