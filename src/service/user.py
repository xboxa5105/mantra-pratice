from typing import Any

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
        records = await self.__record_repo.get_record_summary(user_id, start, end, granularity)
        res = []
        for record in records:
            res.append(
                {
                    "bucket": record.bucket,
                    "total_words": record.total_words,
                    "total_time": record.total_time,
                }
            )
        if n is not None:
            for i in range(n - 1, len(records)):
                word_count_sma = sum([record.word_count for record in records[i - n + 1, i + 1]]) / n
                study_time_sma = sum([record.study_time for record in records[i - n + 1, i + 1]]) / n
                res[i].update(
                    {
                        "word_count_sma": word_count_sma,
                        "study_time_sma": study_time_sma,
                    }
                )
        return res
