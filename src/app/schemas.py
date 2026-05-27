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


class TicketTierCreate(BaseModel):
    name: str
    price: float
    total_seats: int


class TicketTierResponse(BaseModel):
    id: int
    concert_id: int
    name: str
    price: float
    total_seats: int
    available_seats: int
    version: int

    model_config = {"from_attributes": True}


class ConcertCreate(BaseModel):
    title: str
    artist: str
    venue: str
    description: str | None = None
    start_at: datetime
    sale_start_at: datetime


class ConcertResponse(BaseModel):
    id: int
    title: str
    artist: str
    venue: str
    description: str | None
    start_at: datetime
    sale_start_at: datetime
    version: int

    model_config = {"from_attributes": True}


class BookingCreate(BaseModel):
    ticket_tier_id: int
    quantity: int = 1


class BookingResponse(BaseModel):
    id: int
    user_id: int
    concert_id: int
    ticket_tier_id: int
    quantity: int
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
