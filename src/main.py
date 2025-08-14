import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(HTTPException)
async def handle_web_app_error(request: Request, exc: HTTPException):
    logger.error("HTTP Exception: %s", exc)
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Internal Server Error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": int(f"{exc.status_code}000"), "message": str(exc.detail)},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    first = errors[0]
    field = ".".join(str(loc) for loc in first["loc"] if isinstance(loc, str))
    message = f"Field '{field}' {first['msg']}" if field else first["msg"]
    logger.error("Validation Error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"msg": message},
    )


# app.include_router()
