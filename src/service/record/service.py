import hashlib

import arrow
from fastapi import HTTPException

from repository.record import RecordRepository
from repository.user import UserRepository


class RecordService:
    def __init__(self, record_repo: RecordRepository, user_repo: UserRepository):
        self.__record_repo = record_repo
        self.__user_repo = user_repo

    async def create_record(self, user_id: str, word_count: int, study_time: int, timestamp: int | None) -> None:
        user = await self.__user_repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        now = arrow.utcnow()
        if timestamp is not None:
            now = arrow.get(timestamp)
        record_id = self.__generate_record_id(user_id, word_count, study_time, now.int_timestamp)
        if await self.__record_repo.get_record(record_id):
            raise HTTPException(status_code=400, detail=f"Record {record_id} already exists")
        await self.__record_repo.create_record(user.user_id, record_id, word_count, study_time, now.naive)
        return

    def __generate_record_id(self, user_id: str, word_count: int, study_time: int, timestamp: str) -> str:
        base_str = f"{user_id}-{timestamp}-{word_count}-{study_time}"
        return hashlib.sha256(base_str.encode()).hexdigest()
