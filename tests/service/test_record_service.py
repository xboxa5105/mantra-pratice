"""
Record Service 單元測試
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException

from service.record import RecordService


class TestRecordService:
    """Record Service 測試類別"""

    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository, mock_record_repository):
        self.mock_user_repo = mock_user_repository
        self.mock_record_repo = mock_record_repository
        self.record_service = RecordService(mock_record_repository, mock_user_repository)

    @pytest.mark.asyncio
    async def test_create_record_success(self):
        """測試成功建立記錄"""
        # Arrange
        user_id = "test_user_123"
        word_count = 100
        study_time = 3600
        timestamp = 1640995200
        
        # Mock user exists
        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user
        
        # Mock record doesn't exist
        self.mock_record_repo.get_record.return_value = None
        self.mock_record_repo.create_record.return_value = None

        # Act
        result = await self.record_service.create_record(user_id, word_count, study_time, timestamp)

        # Assert
        assert result is None
        self.mock_user_repo.get_user.assert_called_once_with(user_id)
        self.mock_record_repo.get_record.assert_called_once()
        self.mock_record_repo.create_record.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_record_user_not_found(self):
        """測試用戶不存在的情況"""
        # Arrange
        user_id = "nonexistent_user"
        self.mock_user_repo.get_user.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self.record_service.create_record(user_id, 100, 3600, 1640995200)
        
        assert exc_info.value.status_code == 404
        assert f"User {user_id} not found" in str(exc_info.value.detail)