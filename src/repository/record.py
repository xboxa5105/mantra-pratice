from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dependency.db import get_db
from model.record import Record


class RecordRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.__db = db

    async def create_record(self, user_id: str, word_count: int, study_time: int, timestamp: int | None) -> None:
        record = Record(user_id, word_count, study_time, timestamp)
        self.__db.add(record)
        await self.__db.commit()
        return
