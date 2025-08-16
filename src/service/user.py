from typing import Any

import arrow
from fastapi import HTTPException

from constant.granularity import Granularity
from repository.record import RecordRepository
from repository.user import UserRepository


class UserService:
    def __init__(self, record_repo: RecordRepository, user_repo: UserRepository):
        self.__record_repo = record_repo
        self.__user_repo = user_repo

    async def get_user_summary(
        self, user_id: str, start: int, end: int, granularity: Granularity, n: int | None = None
    ) -> list[dict[str, Any]]:
        user = await self.__user_repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        records = await self.__record_repo.get_record_summary(
            user_id, arrow.get(start).naive, arrow.get(end).naive, granularity
        )
        res = []
        for record in records:
            res.append(
                {
                    "date": record.bucket,
                    "word_count": record.total_words,
                    "study_time": record.total_time,
                }
            )
        if n is not None:
            for i in range(n - 1, len(records)):
                word_count_sma = round(sum([record.total_words for record in records[i - n + 1 : i + 1]]) / n, 2)
                study_time_sma = round(sum([record.total_time for record in records[i - n + 1 : i + 1]]) / n, 2)
                res[i].update(
                    {
                        "word_count_sma": word_count_sma,
                        "study_time_sma": study_time_sma,
                    }
                )
        return res
