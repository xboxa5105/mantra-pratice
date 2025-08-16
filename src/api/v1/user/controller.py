import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from api.auth.authenticator import JsonWebTokenAuthenticator
from api.v1.user.schema import GetUserSummaryResponse
from constant.granularity import Granularity
from dependency.service import get_user_service
from service.user import UserService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(JsonWebTokenAuthenticator())],
)


@router.get(
    "/{user_id}/summary",
    summary="Get user summary",
    description="Retrieves the summary of a user's records.",
    response_description="The summary of the user's records.",
    status_code=status.HTTP_200_OK,
    responses={
        200: {"model": GetUserSummaryResponse, "description": "Success"},
        400: {"description": "Bad Request"},
        404: {"description": "User not found"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_user_summary(
    user_id: str,
    start: Annotated[int, Query()],
    end: Annotated[int, Query()],
    granularity: Annotated[Granularity, Query()],
    user: Annotated[UserService, Depends(get_user_service)],
    n: Annotated[int | None, Query()] = None,
) -> JSONResponse:
    summaries = await user.get_user_summary(user_id=user_id, start=start, end=end, granularity=granularity, n=n)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=GetUserSummaryResponse(summary=summaries, total=len(summaries)).model_dump(mode="json"),
    )
