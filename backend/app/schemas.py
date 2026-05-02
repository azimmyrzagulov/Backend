from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import List
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

class UserCreate(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        if not EMAIL_RE.match(value):
            raise ValueError("Invalid email address")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if len(value) > 128:
            raise ValueError("Password must be at most 128 characters")
        return value

class Token(BaseModel):
    access_token: str
    token_type: str


class UserPublic(BaseModel):
    id: int
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class MovieBase(BaseModel):
    title: str
    description: str
    genre: str
    duration: int
    release_date: datetime
    poster_url: str

class MovieCreate(MovieBase):
    pass

class Movie(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class BookingBase(BaseModel):
    movie_id: int
    theater_id: int
    show_time: datetime
    seats: List[str]

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class TheaterBase(BaseModel):
    name: str
    location: str


class TheaterCreate(TheaterBase):
    pass


class TheaterUpdate(TheaterBase):
    pass


class TheaterSchema(TheaterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
