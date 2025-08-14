import uuid

from arrow import arrow
from sqlalchemy import UUID, Column, DateTime, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(UUID(as_uuid=True), default=uuid.uuid4, index=True, unique=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    word_count = Column(Integer, nullable=False)
    study_time = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=arrow.utcnow().naive, nullable=False)
