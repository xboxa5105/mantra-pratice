"""
User Service 單元測試
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from service.user import UserService
from constant.granularity import Granularity

# 設定整個檔案的 async 測試自動使用 asyncio
pytestmark = pytest.mark.asyncio


class TestUserService:
    """User Service 測試類別"""

    @pytest.fixture(autouse=True)
    def setup(self, mock_user_repository, mock_record_repository):
        self.mock_user_repo = mock_user_repository
        self.mock_record_repo = mock_record_repository
        self.user_service = UserService(mock_record_repository, mock_user_repository)

    async def test_get_user_summary_success(self):
        """測試成功取得用戶摘要"""
        # Arrange
        user_id = "test_user_123"
        start = 1640995200
        end = 1672531199
        granularity = Granularity.DAY

        # Mock user exists
        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user

        # Mock record summary
        mock_record1 = MagicMock()
        mock_record1.bucket = "2022-01-01"
        mock_record1.total_words = 100
        mock_record1.total_time = 3600

        mock_record2 = MagicMock()
        mock_record2.bucket = "2022-01-02"
        mock_record2.total_words = 150
        mock_record2.total_time = 4200

        self.mock_record_repo.get_record_summary.return_value = [mock_record1, mock_record2]

        # Act
        result = await self.user_service.get_user_summary(user_id, start, end, granularity)

        # Assert
        expected = [
            {"date": "2022-01-01", "word_count": 100, "study_time": 3600},
            {"date": "2022-01-02", "word_count": 150, "study_time": 4200}
        ]
        assert result == expected

        self.mock_user_repo.get_user.assert_called_once_with(user_id)
        self.mock_record_repo.get_record_summary.assert_called_once_with(
            user_id, start, end, granularity
        )

    async def test_get_user_summary_user_not_found(self):
        """測試用戶不存在的情況"""
        # Arrange
        user_id = "nonexistent_user"
        self.mock_user_repo.get_user.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            await self.user_service.get_user_summary(
                user_id, 1640995200, 1672531199, Granularity.DAY
            )

        assert exc_info.value.status_code == 404
        assert f"User {user_id} not found" in str(exc_info.value.detail)

    async def test_get_user_summary_empty_records(self):
        """測試沒有記錄的情況"""
        # Arrange
        user_id = "test_user_123"
        mock_user = MagicMock()
        mock_user.user_id = user_id
        self.mock_user_repo.get_user.return_value = mock_user
        self.mock_record_repo.get_record_summary.return_value = []

        # Act
        result = await self.user_service.get_user_summary(
            user_id, 1640995200, 1672531199, Granularity.DAY
        )

        # Assert
        assert result == []