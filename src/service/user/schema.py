from datetime import datetime

from pydantic import BaseModel


class Summary(BaseModel):
    date: datetime
    word_count: int
    study_time: int
    word_count_sma: float | None = None
    study_time_sma: float | None = None

    class Config:
        orm_mode = True
