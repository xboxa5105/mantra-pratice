from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from constant.granularity import Granularity
from dependency.db import get_db
from model.record import Record


class RecordRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.__db = db

    async def get_record(self, record_id: str) -> Record | None:
        stmt = select(Record).where(Record.record_id == record_id)
        return await self.__db.scalar(stmt)

    async def get_record_summary(self, user_id: str, start: int, end: int, granularity: Granularity) -> list[Record]:
        stmt = (
            select(
                func.date_trunc(granularity, Record.timestamp).label("bucket"),
                func.sum(Record.word_count).label("total_words"),
                func.sum(Record.study_time).label("total_time")
            )
            .where(Record.user_id == user_id, Record.timestamp >= start, Record.timestamp < end)
            .group_by("bucket")
            .order_by("bucket")
        )
        rows = await self.__db.execute(stmt)
        result = rows.all()
        return result

    async def create_record(
        self, user_id: str, record_id: str, word_count: int, study_time: int, timestamp: int
    ) -> None:
        record = Record(
            user_id=user_id, record_id=record_id, word_count=word_count, study_time=study_time, timestamp=timestamp
        )
        self.__db.add(record)
        await self.__db.commit()
        return
