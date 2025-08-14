from fastapi import HTTPException

from repository.user import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.__user_repo = user_repo

    async def get_user_summary(self, user_id: str, word_count: int, study_time: int, timestamp: int | None):
        user = await self.__user_repo.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
