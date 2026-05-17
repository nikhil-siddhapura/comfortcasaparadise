from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from models.tables import Booking, Product, BookingService
from schemas.schemas import BookingCreate, BookingOut, BookingUpdate
from routers.dependencies import get_current_user, require_admin

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if payload.adults + payload.children < 3:
        raise HTTPException(400, "Minimum 3 persons required (adults + children)")
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")
    if product.available_rooms < 1:
        raise HTTPException(400, "No rooms available for this product")
    nights = (payload.check_out - payload.check_in).days
    if nights < 1:
        raise HTTPException(400, "Minimum 1 night stay required")
    total_price = float(product.price) * nights
    booking = Booking(
        user_id=user.id, product_id=payload.product_id,
        check_in=payload.check_in, check_out=payload.check_out,
        adults=payload.adults, children=payload.children, total_price=total_price
    )
    db.add(booking)
    product.available_rooms -= 1
    db.commit(); db.refresh(booking)
    for sid in payload.service_ids:
        db.add(BookingService(booking_id=booking.id, service_id=sid))
    db.commit()
    return booking

@router.get("/my", response_model=List[BookingOut])
def my_bookings(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Booking).filter(Booking.user_id == user.id).order_by(Booking.created_at.desc()).all()

@router.get("/", response_model=List[BookingOut])
def all_bookings(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Booking).order_by(Booking.created_at.desc()).all()

@router.put("/{booking_id}/status", response_model=BookingOut)
def update_booking_status(booking_id: int, payload: BookingUpdate,
                           db: Session = Depends(get_db), admin=Depends(require_admin)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    # Restore room if rejecting a previously pending/approved booking
    if payload.status == "rejected" and booking.status != "rejected":
        product = db.query(Product).filter(Product.id == booking.product_id).first()
        if product:
            product.available_rooms += 1
    booking.status        = payload.status
    booking.admin_message = payload.admin_message
    db.commit(); db.refresh(booking)
    return booking
