from pydantic import BaseModel


class AuthData(BaseModel):
    user_id: str = ""


class JsonWebToken(BaseModel):
    user_id: str
    exp: int
