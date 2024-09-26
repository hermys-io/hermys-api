from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class KnowledgeNotFound(Exception):
    ...


def bind_knowledge_exceptions(app: FastAPI):
    @app.exception_handler(KnowledgeNotFound)
    def knowledge_not_found(_request: Request, _exc: KnowledgeNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'Knowledge not found',
                'code': 'KNOWLEDGE_NOT_FOUNT',
            },
        )
