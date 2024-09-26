from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class AuditNotFound(Exception):
    ...


def bind_audit_exceptions(app: FastAPI):
    @app.exception_handler(AuditNotFound)
    def audit_not_found(_request: Request, _exc: AuditNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'audit not found',
                'code': 'AUDIT_NOT_FOUNT',
            },
        )
