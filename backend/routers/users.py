from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil, os, uuid

from database.connection import get_db
from models.tables import User
from schemas.schemas import UserOut, UserUpdate
from routers.dependencies import get_current_user, require_admin

router     = APIRouter(prefix="/users", tags=["Users"])
UPLOAD_DIR = "uploads/profiles"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/me", response_model=UserOut)
def get_profile(user=Depends(get_current_user)):
    return user

@router.put("/me", response_model=UserOut)
def update_profile(payload: UserUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit(); db.refresh(user)
    return user

@router.post("/me/avatar", response_model=UserOut)
def upload_avatar(image: UploadFile = File(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    ext        = image.filename.rsplit(".", 1)[-1].lower()
    filename   = f"{uuid.uuid4()}.{ext}"
    image_path = f"{UPLOAD_DIR}/{filename}"
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    user.profile_image = image_path
    db.commit(); db.refresh(user)
    return user

@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(User).order_by(User.created_at.desc()).all()
