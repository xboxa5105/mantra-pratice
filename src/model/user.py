import uuid

import arrow
from sqlalchemy import UUID, Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=arrow.utcnow().naive, nullable=False)
