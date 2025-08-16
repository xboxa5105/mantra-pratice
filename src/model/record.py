import arrow
from sqlalchemy import UUID, Column, DateTime, Integer, String

from model.base import Base


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, unique=True, index=True)
    user_id = Column(UUID(as_uuid=True), index=True, nullable=False)
    word_count = Column(Integer, nullable=False)
    study_time = Column(Integer, nullable=False)
    date = Column(DateTime, default=arrow.utcnow().naive, nullable=False)
