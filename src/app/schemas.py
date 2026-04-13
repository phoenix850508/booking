from datetime import date

from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    birthday: date


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
