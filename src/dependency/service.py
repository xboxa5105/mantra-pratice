from typing import Annotated

from fastapi import Depends

from dependency.repository import get_record_repository, get_user_repository
from repository.record import RecordRepository
from repository.user import UserRepository
from service.record import RecordService
from service.user import UserService


def get_record_service(
    record_repo: Annotated[RecordRepository, Depends(get_record_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> RecordService:
    return RecordService(record_repo, user_repo)


def get_user_service(
    record_repo: Annotated[RecordRepository, Depends(get_record_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(record_repo, user_repo)
