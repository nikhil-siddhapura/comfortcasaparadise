from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database.connection import get_db
from models.tables import Contact
from schemas.schemas import ContactCreate, ContactOut, ContactReply
from routers.dependencies import require_admin

router = APIRouter(prefix="/contacts", tags=["Contacts"])

@router.post("/", response_model=ContactOut, status_code=201)
def send_message(payload: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**payload.model_dump())
    db.add(contact); db.commit(); db.refresh(contact)
    return contact

@router.get("/", response_model=List[ContactOut])
def get_contacts(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Contact).order_by(Contact.created_at.desc()).all()

@router.put("/{contact_id}/reply", response_model=ContactOut)
def reply_contact(contact_id: int, payload: ContactReply,
                  db: Session = Depends(get_db), admin=Depends(require_admin)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(404, "Message not found")
    contact.admin_reply = payload.admin_reply
    contact.is_read     = True
    db.commit(); db.refresh(contact)
    return contact
