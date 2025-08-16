from pydantic import BaseModel


class Summary(BaseModel):
    date: str
    word_count: int
    study_time: int
    word_count_sma: float | None = None
    study_time_sma: float | None = None


class GetUserSummaryResponse(BaseModel):
    summary: list[Summary]
    total: int
