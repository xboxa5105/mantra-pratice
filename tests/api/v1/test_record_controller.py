from unittest.mock import AsyncMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from dependency.service import get_record_service
from main import app


class TestRecordController:
    @pytest.fixture(autouse=True)
    def setup(self, mock_record_service):
        self.mock_record_service = mock_record_service
        self.base_url = "/api/v1/records"

        app.dependency_overrides[get_record_service] = lambda: self.mock_record_service

        self.client = TestClient(app)

        yield

        app.dependency_overrides.clear()

    def test_create_record_success(self, mock_jwt_header: dict[str, str]):
        user_id = "test_user_123"
        word_count = 100
        study_time = 3600
        timestamp = 1640995200

        self.mock_record_service.create_record = AsyncMock(return_value=None)

        response = self.client.post(
            f"{self.base_url}/{user_id}",
            json={"word_count": word_count, "study_time": study_time, "timestamp": timestamp},
            headers=mock_jwt_header,
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {}

    def test_create_record_without_timestamp(self, mock_jwt_header: dict[str, str]):
        user_id = "test_user_123"
        word_count = 150
        study_time = 4200

        self.mock_record_service.create_record = AsyncMock(return_value=None)

        response = self.client.post(
            f"{self.base_url}/{user_id}",
            json={"word_count": word_count, "study_time": study_time},
            headers=mock_jwt_header,
        )

        assert response.status_code == status.HTTP_201_CREATED

    def test_create_record_service_error(self, mock_jwt_header: dict[str, str]):
        user_id = "test_user_123"
        self.mock_record_service.create_record = AsyncMock(side_effect=Exception("Service error"))

        with pytest.raises(Exception, match="Service error"):
             self.client.post(
                f"{self.base_url}/{user_id}",
                json={"word_count": 100, "study_time": 3600},
                headers=mock_jwt_header,
            )

    def test_create_record_invalid_data(self, mock_jwt_header: dict[str, str]):
        user_id = "test_user_123"

        response = self.client.post(
            f"{self.base_url}/{user_id}",
            json={
                "word_count": "invalid",  # 應該是整數
                "study_time": 3600,
            },
            headers=mock_jwt_header,
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
