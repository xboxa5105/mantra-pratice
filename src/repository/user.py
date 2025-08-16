from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from dependency.db import get_db
from model.user import User


class UserRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.__db = db

    async def get_user(self, user_id: str) -> User | None:
        stmt = select(User).where(User.user_id == user_id)
        return await self.__db.scalar(stmt)
