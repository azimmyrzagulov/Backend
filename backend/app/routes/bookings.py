from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Booking
from ..schemas import Booking as BookingSchema, BookingCreate
from ..auth import get_current_user
from ..config import settings

router = APIRouter()

@router.get("/", response_model=list[BookingSchema])
def get_bookings(
    skip: int = 0,
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    bookings = db.query(Booking).filter(Booking.user_id == current_user.id).offset(skip).limit(limit).all()
    return bookings

@router.post("/", response_model=BookingSchema)
def create_booking(booking: BookingCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    bookings_query = db.query(Booking).filter(
        Booking.movie_id == booking.movie_id,
        Booking.theater_id == booking.theater_id,
        Booking.show_time == booking.show_time,
    )

    if not settings.database_url.startswith("sqlite"):
        bookings_query = bookings_query.with_for_update()

    existing_bookings = bookings_query.all()
    requested_seats = set(booking.seats)

    for existing_booking in existing_bookings:
        if requested_seats.intersection(existing_booking.seats):
            raise HTTPException(status_code=409, detail="One or more seats are already booked")

    db_booking = Booking(**booking.model_dump(), user_id=current_user.id)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
