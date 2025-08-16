import logging
import logging.config
import uuid

from fastapi import FastAPI, Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.v1.router import router as v1_router
from core.contextvar.trace_id import trace_id_ctx
from util.logger import logger_config

logging.config.dictConfig(logger_config())
logger = logging.getLogger(__name__)

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    trace_id = request.headers.get("X-Trace-Id", str(uuid.uuid4()))
    trace_id_ctx.set(trace_id)
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    trace_id_ctx.set("-")
    return response


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
        content={"message": str(exc.detail)},
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


app.include_router(v1_router, prefix="/api/v1")
