import pytest
import jwt
import time
from unittest.mock import MagicMock, patch
from fastapi import HTTPException, Request
from fastapi.datastructures import Headers

from api.auth.authenticator import JsonWebTokenAuthenticator
from api.auth.schema import AuthData


class TestJsonWebTokenAuthenticator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.authenticator = JsonWebTokenAuthenticator()

    def test_get_jwt_success(self):
        headers = Headers({"authorization": "Bearer test_token_123"})

        token = self.authenticator.get_jwt(headers)

        assert token == "test_token_123"

    def test_get_jwt_missing_header(self):
        headers = Headers({})

        with pytest.raises(HTTPException) as exc_info:
            self.authenticator.get_jwt(headers)

        assert exc_info.value.status_code == 401
        assert "Request header should contain jwt token" in str(exc_info.value.detail)

    def test_get_jwt_invalid_format(self):
        headers = Headers({"authorization": "InvalidFormat"})

        with pytest.raises(HTTPException) as exc_info:
            self.authenticator.get_jwt(headers)

        assert exc_info.value.status_code == 401
        assert "Invalid Authorization header" in str(exc_info.value.detail)

    def test_get_jwt_non_bearer_token(self):
        headers = Headers({"authorization": "Basic dGVzdA=="})

        token = self.authenticator.get_jwt(headers)

        assert token == ""

    @patch('jwt.decode')
    def test_validate_jwt_token_success(self, mock_jwt_decode):
        token = "valid_token"
        current_time = int(time.time())
        mock_payload = {
            "user_id": "test_user_123",
            "exp": current_time + 3600
        }
        mock_jwt_decode.return_value = mock_payload

        result = self.authenticator.validate_jwt_token(token)

        assert result == mock_payload
        mock_jwt_decode.assert_called_once_with(token, algorithms=["HS256"])

    @patch('jwt.decode')
    def test_validate_jwt_token_expired(self, mock_jwt_decode):
        token = "expired_token"
        mock_jwt_decode.side_effect = jwt.ExpiredSignatureError("Token has expired")

        result = self.authenticator.validate_jwt_token(token)

        assert result is None

    @patch('jwt.decode')
    def test_validate_jwt_token_invalid(self, mock_jwt_decode):
        token = "invalid_token"
        mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")

        result = self.authenticator.validate_jwt_token(token)

        assert result is None

    @patch.object(JsonWebTokenAuthenticator, 'validate_jwt_token')
    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_success(self, mock_get_jwt, mock_validate_jwt):
        headers = Headers({"authorization": "Bearer valid_token"})
        mock_get_jwt.return_value = "valid_token"
        mock_validate_jwt.return_value = {
            "user_id": "test_user_123",
            "exp": int(time.time()) + 3600
        }

        result = self.authenticator.verify(headers)

        assert isinstance(result, AuthData)
        assert result.user_id == "test_user_123"
        mock_get_jwt.assert_called_once_with(headers)
        mock_validate_jwt.assert_called_once_with("valid_token")

    @patch.object(JsonWebTokenAuthenticator, 'validate_jwt_token')
    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_invalid_token(self, mock_get_jwt, mock_validate_jwt):
        headers = Headers({"authorization": "Bearer invalid_token"})
        mock_get_jwt.return_value = "invalid_token"
        mock_validate_jwt.return_value = None

        with pytest.raises(HTTPException) as exc_info:
            self.authenticator.verify(headers)

        assert exc_info.value.status_code == 401
        assert "Invalid JWT token" in str(exc_info.value.detail)
        mock_get_jwt.assert_called_once_with(headers)
        mock_validate_jwt.assert_called_once_with("invalid_token")

    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_missing_header(self, mock_get_jwt):
        headers = Headers({})
        mock_get_jwt.side_effect = HTTPException(
            status_code=401,
            detail="Request header should contain jwt token"
        )

        with pytest.raises(HTTPException) as exc_info:
            self.authenticator.verify(headers)

        assert exc_info.value.status_code == 401
        assert "Request header should contain jwt token" in str(exc_info.value.detail)

    @patch.object(JsonWebTokenAuthenticator, 'validate_jwt_token')
    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_malformed_jwt_payload(self, mock_get_jwt, mock_validate_jwt):
        headers = Headers({"authorization": "Bearer malformed_token"})
        mock_get_jwt.return_value = "malformed_token"

        mock_validate_jwt.return_value = {"exp": int(time.time()) + 3600}

        with pytest.raises(Exception):
            self.authenticator.verify(headers)

    @patch.object(JsonWebTokenAuthenticator, 'validate_jwt_token')
    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_with_different_user_ids(self, mock_get_jwt, mock_validate_jwt):
        headers = Headers({"authorization": "Bearer token_user_456"})
        mock_get_jwt.return_value = "token_user_456"
        mock_validate_jwt.return_value = {
            "user_id": "different_user_456",
            "exp": int(time.time()) + 3600
        }

        result = self.authenticator.verify(headers)

        assert isinstance(result, AuthData)
        assert result.user_id == "different_user_456"

    @patch.object(JsonWebTokenAuthenticator, 'validate_jwt_token')
    @patch.object(JsonWebTokenAuthenticator, 'get_jwt')
    def test_verify_with_empty_user_id(self, mock_get_jwt, mock_validate_jwt):
        headers = Headers({"authorization": "Bearer token_empty_user"})
        mock_get_jwt.return_value = "token_empty_user"
        mock_validate_jwt.return_value = {
            "user_id": "",
            "exp": int(time.time()) + 3600
        }


        result = self.authenticator.verify(headers)


        assert isinstance(result, AuthData)
        assert result.user_id == ""