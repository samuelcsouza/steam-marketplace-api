import importlib

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from src.utils import api_errors

app = FastAPI()


@app.exception_handler(HTTPException)
async def api_exception_handler(request: Request, exception: HTTPException) -> JSONResponse:

    error_status_code, error_detail = exception.status_code, exception.detail

    if isinstance(error_detail, str):
        if error_status_code == api_errors.ErrorRouteNotFound.status_code:
            error_detail = api_errors.ErrorRouteNotFound.error
        elif error_status_code == api_errors.ErrorMethodNotAllowed.status_code:
            error_detail = api_errors.ErrorMethodNotAllowed.error

    return JSONResponse(
        status_code=error_status_code,
        content={"error": error_detail},
    )


@app.exception_handler(api_errors.BusinessException)
async def business_exception_handler(request: Request, exception: api_errors.BusinessException) -> JSONResponse:
    try:
        api_errors.raise_error_response(exception, str(exception) or None)
    except HTTPException as e:
        return await api_exception_handler(request, e)

api_module = importlib.import_module("src.routers.api")

app.include_router(api_module.api_router)
