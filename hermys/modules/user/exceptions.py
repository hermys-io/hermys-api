from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class UserAlreadyExists(Exception):
    ...


class UserNotFound(Exception):
    ...


def bind_user_exceptions(app: FastAPI):
    @app.exception_handler(UserAlreadyExists)
    def user_already_exists(
        _request: Request, _exc: UserAlreadyExists
    ):   # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'detail': 'User already exists',
                'code': 'USER_ALREADY_EXISTS',
            },
        )

    @app.exception_handler(UserNotFound)
    def user_not_found(_request: Request, _exc: UserNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'User not found',
                'code': 'USER_NOT_FOUNT',
            },
        )
