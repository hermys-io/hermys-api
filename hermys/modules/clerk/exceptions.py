from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class ClerkAlreadyExists(Exception):
    ...


class ClerkNotFound(Exception):
    ...


def bind_clerk_exceptions(app: FastAPI):
    @app.exception_handler(ClerkAlreadyExists)
    def clerk_already_exists(  # type: ignore
        _request: Request, _exc: ClerkAlreadyExists
    ):
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'detail': 'Clerk already exists',
                'code': 'CLERK_ALREADY_EXISTS',
            },
        )

    @app.exception_handler(ClerkNotFound)
    def clerk_not_found(_request: Request, _exc: ClerkNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'Clerk not found',
                'code': 'CLERK_NOT_FOUNT',
            },
        )
