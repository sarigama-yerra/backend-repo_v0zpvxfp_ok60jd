"""
Database Schemas for Cinema Booking System

Each Pydantic model below corresponds to a MongoDB collection. The collection
name is the lowercase of the class name (e.g., Movie -> "movie").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime


class Movie(BaseModel):
    """Movies available for booking"""
    title: str = Field(..., description="Movie title")
    description: Optional[str] = Field(None, description="Short synopsis")
    duration_mins: int = Field(..., ge=1, description="Duration in minutes")
    genre: Optional[str] = Field(None, description="Primary genre")
    rating: Optional[str] = Field(None, description="Content rating, e.g., PG-13")
    poster_url: Optional[str] = Field(None, description="Poster image URL")


class Showtime(BaseModel):
    """Showtime for a specific movie"""
    movie_id: str = Field(..., description="ID of the movie (string ObjectId)")
    start_time: datetime = Field(..., description="Show start time (ISO 8601)")
    auditorium: str = Field(..., description="Auditorium identifier")
    rows: int = Field(8, ge=1, le=26, description="Number of seating rows")
    cols: int = Field(12, ge=1, le=30, description="Number of seats per row")
    price: float = Field(12.0, ge=0, description="Ticket price")


class Booking(BaseModel):
    """Booking made by a customer for one showtime"""
    showtime_id: str = Field(..., description="ID of the showtime (string ObjectId)")
    customer_name: str = Field(..., description="Customer full name")
    customer_email: EmailStr = Field(..., description="Customer email")
    seats: List[str] = Field(..., min_items=1, description="List of seat codes like A1, A2")
    status: str = Field("confirmed", description="Booking status")


# Example original schemas kept for reference compatibility in tooling
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True


class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
