from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependency.db import get_db
from repository.record import RecordRepository
from repository.user import UserRepository


def get_record_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> RecordRepository:
    return RecordRepository(db)


def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)
