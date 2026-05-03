from datetime import date, datetime

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


class ConcertCreate(BaseModel):
    title: str
    artist: str
    venue: str
    description: str | None = None
    start_at: datetime
    total_seats: int
    price: float


class ConcertResponse(BaseModel):
    id: int
    title: str
    artist: str
    venue: str
    description: str | None
    start_at: datetime
    total_seats: int
    available_seats: int
    price: float

    model_config = {"from_attributes": True}
