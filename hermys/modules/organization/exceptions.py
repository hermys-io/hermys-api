from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class OrganizationAlreadyExists(Exception):
    ...


class OrganizationNotFound(Exception):
    ...


def bind_organization_exceptions(app: FastAPI):
    @app.exception_handler(OrganizationAlreadyExists)
    def organization_already_exists(  # type: ignore
        _request: Request, _exc: OrganizationAlreadyExists
    ):
        return ORJSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                'detail': 'Organization already exists',
                'code': 'ORGANIZATION_ALREADY_EXISTS',
            },
        )

    @app.exception_handler(OrganizationNotFound)
    def organization_not_found(_request: Request, _exc: OrganizationNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'Organization not found',
                'code': 'ORGANIZATION_NOT_FOUNT',
            },
        )
