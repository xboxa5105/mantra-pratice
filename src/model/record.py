import arrow
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    record_id = Column(String, unique=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    word_count = Column(Integer, nullable=False)
    study_time = Column(Integer, nullable=False)
    timestamp = Column(DateTime, default=arrow.utcnow().naive, nullable=False)
