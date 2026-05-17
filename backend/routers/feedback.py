from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from models.tables import Feedback, Booking
from schemas.schemas import FeedbackCreate, FeedbackOut
from routers.dependencies import get_current_user

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.post("/", response_model=FeedbackOut, status_code=201)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    booking = db.query(Booking).filter(
        Booking.id == payload.booking_id,
        Booking.user_id == user.id,
        Booking.status == "approved"
    ).first()
    if not booking:
        raise HTTPException(403, "You can only review your own approved bookings")
    fb = Feedback(user_id=user.id, **payload.model_dump())
    db.add(fb); db.commit(); db.refresh(fb)
    return fb

@router.get("/", response_model=List[FeedbackOut])
def get_all_feedback(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()
