from unittest.mock import MagicMock

import arrow
import pytest
from fastapi import HTTPException

from constant.granularity import Granularity
from service.user.service import UserService


class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository, mock_record_repository):
        self.mock_user_repo = mock_user_repository
        self.mock_record_repo = mock_record_repository
        self.user_service = UserService(mock_record_repository, mock_user_repository)

    async def test_get_user_summary_success(self):
        user_id = "test_user_123"
        start = 1640995200
        end = 1672531199
        granularity = Granularity.DAY

        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user

        mock_record1 = MagicMock()
        mock_record1.bucket = "2022-01-01"
        mock_record1.total_words = 100
        mock_record1.total_time = 3600

        mock_record2 = MagicMock()
        mock_record2.bucket = "2022-01-02"
        mock_record2.total_words = 150
        mock_record2.total_time = 4200

        self.mock_record_repo.get_record_summary.return_value = [mock_record1, mock_record2]

        result = await self.user_service.get_user_summary(user_id, start, end, granularity)

        expected = [
            {
                "date": "2022-01-01T00:00:00",
                "word_count": 100,
                "study_time": 3600,
                "study_time_sma": None,
                "word_count_sma": None,
            },
            {
                "date": "2022-01-02T00:00:00",
                "word_count": 150,
                "study_time": 4200,
                "study_time_sma": None,
                "word_count_sma": None,
            },
        ]
        assert result == expected

        self.mock_user_repo.get_user.assert_called_once_with(user_id)
        self.mock_record_repo.get_record_summary.assert_called_once_with(
            user_id, arrow.get(start).naive, arrow.get(end).naive, granularity
        )

    async def test_get_user_summary_user_not_found(self):
        user_id = "nonexistent_user"
        self.mock_user_repo.get_user.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.get_user_summary(user_id, 1640995200, 1672531199, Granularity.DAY)

        assert exc_info.value.status_code == 404
        assert f"User {user_id} not found" in str(exc_info.value.detail)

    async def test_get_user_summary_empty_records(self):
        user_id = "test_user_123"
        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user
        self.mock_record_repo.get_record_summary.return_value = []

        result = await self.user_service.get_user_summary(user_id, 1640995200, 1672531199, Granularity.DAY)

        assert result == []
