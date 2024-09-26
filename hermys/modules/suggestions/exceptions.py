from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse


class SuggestionNotFound(Exception):
    ...


def bind_suggestion_exceptions(app: FastAPI):
    @app.exception_handler(SuggestionNotFound)
    def suggestion_not_found(_request: Request, _exc: SuggestionNotFound):  # type: ignore
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                'detail': 'suggestion not found',
                'code': 'SUGGESTION_NOT_FOUNT',
            },
        )
