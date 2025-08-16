import logging
import time

import jwt
from fastapi import HTTPException, Request, status
from fastapi.datastructures import Headers

from api.auth.schema import AuthData, JsonWebToken

logger = logging.getLogger(__name__)


class JsonWebTokenAuthenticator:
    def get_jwt(self, headers: Headers) -> str:
        auth_header = headers.get("Authorization")
        if not auth_header:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Request header should contain jwt token"},
            )
        try:
            token_type, token = auth_header.split(" ")
            if token_type.lower() == "bearer":
                return token
            return ""
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Invalid Authorization header"}
            )

    def validate_jwt_token(self, token: str) -> dict | None:
        try:
            print(token)
            identifier_token = jwt.decode(
                token,
                algorithms=["HS256"],
            )
            logger.info("Identifier Token: %s", identifier_token)
            expired_time = identifier_token.get("exp", None)
            # Check expired_time is expired or not
            if expired_time is None:
                raise jwt.InvalidTokenError("Token has no expired time field: exp")
            if expired_time < int(time.time()):
                raise jwt.ExpiredSignatureError("Token has expired")
            return identifier_token
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
        except jwt.InvalidTokenError as e:
            logger.warning("Invalid Token: %s", e)
        return None

    def verify(self, headers: Headers) -> AuthData:
        jwt = self.validate_jwt_token(self.get_jwt(headers))

        if jwt is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Invalid JWT token"},
            )

        token = JsonWebToken(**jwt)

        return AuthData(
            user_id=token.user_id,
        )

    async def __call__(self, request: Request):
        return self.verify(request.headers)
