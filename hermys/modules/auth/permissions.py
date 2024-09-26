from functools import wraps
from typing import Any, Callable, List, TypeVar

from hermys.modules.auth.exceptions import DoesNotHavePermission
from hermys.modules.user.enums import UserRoleEnum
from hermys.modules.user.schemas import UserInternal

F = TypeVar('F', bound=Callable[..., Any])


def with_permissions(roles: List[UserRoleEnum]) -> Callable[[F], F]:
    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            current_user = kwargs.get('current_user')
            _current_user = kwargs.get('_current_user')

            user: UserInternal | None = current_user or _current_user

            if not user:
                raise EnvironmentError('Current online user was not provided')

            if user.role == UserRoleEnum.GOD or user.role in roles:
                result = await func(*args, **kwargs)
                return result

            raise DoesNotHavePermission()

        return wrapper  # type: ignore

    return decorator
