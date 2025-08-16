"""
測試配置文件，包含共用的 fixtures 和設定
"""
import arrow
import jwt
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, MagicMock

from main import app
from service.user import UserService
from service.record import RecordService
from repository.user import UserRepository
from repository.record import RecordRepository


@pytest.fixture
def mock_user_repository() -> AsyncMock:
    """Mock UserRepository"""
    mock_repo = AsyncMock(spec=UserRepository)
    return mock_repo


@pytest.fixture
def mock_record_repository() -> AsyncMock:
    """Mock RecordRepository"""
    mock_repo = AsyncMock(spec=RecordRepository)
    return mock_repo


@pytest.fixture
def mock_user_service(mock_user_repository, mock_record_repository) -> UserService:
    """Mock UserService"""
    return UserService(mock_record_repository, mock_user_repository)


@pytest.fixture
def mock_record_service(mock_user_repository, mock_record_repository) -> RecordService:
    """Mock RecordService"""
    return RecordService(mock_record_repository, mock_user_repository)


@pytest.fixture
def mock_jwt_header() -> dict[str, str]:
    future_time = arrow.utcnow().int_timestamp + 3600
    mock_jwt = jwt.encode({
        "user_id": "test-user-id",
        "exp": future_time
    }, key="", algorithm="HS256")
    return {"Authorization": f"Bearer {mock_jwt}"}
