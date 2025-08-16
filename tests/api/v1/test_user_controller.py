import arrow
import pytest
from unittest.mock import AsyncMock, patch
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from constant.granularity import Granularity
from dependency.service import get_user_service


class TestUserController:
    @pytest.fixture(autouse=True)
    def setup(self, mock_user_service):
        self.mock_user_service = mock_user_service
        self.base_url = "/api/v1/users"
        self.client = TestClient(app)

        # Override service dependency
        app.dependency_overrides[get_user_service] = lambda: self.mock_user_service

        yield

        # Cleanup
        app.dependency_overrides.clear()

    def test_get_user_summary_success(self, mock_jwt_header):
        user_id = "test_user_123"
        start = 1640995200  # 2022-01-01
        end = 1672531199  # 2022-12-31
        granularity = Granularity.DAY

        expected_summary = [
            {"date": "2022-01-01", "word_count": 100, "study_time": 3600},
            {"date": "2022-01-02", "word_count": 150, "study_time": 4200},
        ]
        self.mock_user_service.get_user_summary = AsyncMock(return_value=expected_summary)
        # Act
        response = self.client.get(
            f"{self.base_url}/{user_id}/summary", params={"start": start, "end": end, "granularity": granularity.value},
            headers=mock_jwt_header
        )
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        for summary in expected_summary:
            summary.update({
                "study_time_sma": None,
                "word_count_sma": None,
            })
        assert response_data["summary"] == expected_summary
        assert response_data["total"] == len(expected_summary)
