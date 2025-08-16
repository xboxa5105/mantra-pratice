import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse

from api.auth.authenticator import JsonWebTokenAuthenticator
from dependency.service import get_record_service
from service.record import RecordService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/records",
    tags=["Record"],
    dependencies=[Depends(JsonWebTokenAuthenticator())],
)


@router.post(
    "/{user_id}",
    summary="Add a new record for a user",
    description="Adds a new record for a user.",
    response_description="The created record.",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Record created successfully"},
        400: {"description": "Bad Request"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def create_record(
    user_id: str,
    record: Annotated[RecordService, Depends(get_record_service)],
    word_count: Annotated[int, Body()],
    study_time: Annotated[int, Body()],
    timestamp: Annotated[int, Body()] = None,
) -> JSONResponse:
    await record.create_record(user_id=user_id, word_count=word_count, study_time=study_time, timestamp=timestamp)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={},
    )
