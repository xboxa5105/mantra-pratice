from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from service.record.service import RecordService


class TestRecordService:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository: AsyncMock, mock_record_repository: AsyncMock):
        self.mock_user_repo = mock_user_repository
        self.mock_record_repo = mock_record_repository
        self.record_service = RecordService(mock_record_repository, mock_user_repository)

    @pytest.mark.asyncio
    async def test_create_record_success(self):
        user_id = "test_user_123"
        word_count = 100
        study_time = 3600
        timestamp = 1640995200

        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user

        self.mock_record_repo.get_record.return_value = None
        self.mock_record_repo.create_record.return_value = None

        result = await self.record_service.create_record(user_id, word_count, study_time, timestamp)

        assert result is None
        self.mock_user_repo.get_user.assert_called_once_with(user_id)
        self.mock_record_repo.get_record.assert_called_once()
        self.mock_record_repo.create_record.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_record_user_not_found(self):
        user_id = "nonexistent_user"
        self.mock_user_repo.get_user.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            await self.record_service.create_record(user_id, 100, 3600, 1640995200)

        assert exc_info.value.status_code == 404
        assert f"User {user_id} not found" in str(exc_info.value.detail)
