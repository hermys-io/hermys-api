from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class IncorrectUsernameOrPassword(Exception):
    ...


def bind_auth_exceptions(app: FastAPI):
    @app.exception_handler(IncorrectUsernameOrPassword)
    def incorrect_username_or_password(
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
