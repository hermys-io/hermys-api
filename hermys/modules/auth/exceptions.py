from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class IncorrectUsernameOrPassword(Exception):
    ...


class DoesNotHavePermission(Exception):
    ...


class Unauthorized(Exception):
    ...


def bind_auth_exceptions(app: FastAPI):
    @app.exception_handler(IncorrectUsernameOrPassword)
    def incorrect_username_or_password(  # type: ignore
        _request: Request,
        _exc: IncorrectUsernameOrPassword,
    ):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                'detail': 'Incorrect username or password',
                'code': 'USERNAME_OR_PASSWORD_ERROR',
            },
        )

    @app.exception_handler(DoesNotHavePermission)
    def does_not_have_permission(  # type: ignore
        _request: Request,
        _exc: DoesNotHavePermission,
    ):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={
                'detail': 'Does not have permission',
                'code': 'PERMISSION_ERROR',
            },
        )

    @app.exception_handler(Unauthorized)
    def unauthorized(  # type: ignore
        _request: Request,
        _exc: Unauthorized,
    ):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                'detail': 'Incorrect credentials',
                'code': 'UNAUTHORIZED_ERROR',
            },
        )
