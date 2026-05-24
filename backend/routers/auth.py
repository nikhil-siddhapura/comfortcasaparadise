from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets, os

from database.connection import get_db
from models.tables import User, PasswordReset
from schemas.schemas import (UserRegister, UserLogin, AdminLogin,
                              Token, ForgotPassword, ResetPassword, UserOut)
from passlib.context import CryptContext
from jose import jwt

router         = APIRouter(prefix="/auth", tags=["Authentication"])
pwd_context    = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY     = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM      = os.getenv("ALGORITHM", "HS256")
EXPIRE_MIN     = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

def hash_password(p):        return pwd_context.hash(p)
def verify_password(p, h):   return pwd_context.verify(p, h)

def create_token(data, minutes=None):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=minutes or EXPIRE_MIN)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ── Register ──────────────────────────────────────────────────
@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(400, "Email already registered")
    user = User(full_name=payload.full_name, email=payload.email,
                password=hash_password(payload.password), phone=payload.phone)
    db.add(user); db.commit(); db.refresh(user)
    return user

# ── User Login ────────────────────────────────────────────────
@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password):
        raise HTTPException(401, "Invalid email or password")
    if not user.is_active:
        raise HTTPException(403, "Account is deactivated")
    token = create_token({"sub": user.email, "role": "user", "id": user.id})
    return {"access_token": token, "token_type": "bearer", "role": "user"}

# ── Admin Login ───────────────────────────────────────────────
@router.post("/admin-login", response_model=Token)
def admin_login(payload: AdminLogin):
    if payload.username != ADMIN_USERNAME or payload.password != ADMIN_PASSWORD:
        raise HTTPException(401, "Invalid admin credentials")
    token = create_token({"sub": payload.username, "role": "admin"})
    return {"access_token": token, "token_type": "bearer", "role": "admin"}

# ── Forgot Password ───────────────────────────────────────────
# Generates a token and returns it in response (no email server needed)
@router.post("/forgot-password")
def forgot_password(payload: ForgotPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(404, "No account found with this email")
    # Invalidate any old unused tokens for this email
    db.query(PasswordReset).filter(
        PasswordReset.email == payload.email,
        PasswordReset.used  == False
    ).update({"used": True})
    db.commit()
    # Create new token valid for 30 minutes
    token   = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=30)
    db.add(PasswordReset(email=payload.email, token=token, expires_at=expires))
    db.commit()
    return {
        "message"   : "Password reset token generated successfully.",
        "token"     : token,          # shown on screen for copy-paste
        "expires_at": str(expires),
        "note"      : "Copy this token and paste it in the Reset Password section below."
    }

# ── Reset Password ────────────────────────────────────────────
@router.post("/reset-password")
def reset_password(payload: ResetPassword, db: Session = Depends(get_db)):
    record = db.query(PasswordReset).filter(
        PasswordReset.token == payload.token,
        PasswordReset.used  == False
    ).first()
    if not record:
        raise HTTPException(400, "Invalid token. Please generate a new one.")
    if record.expires_at < datetime.utcnow():
        raise HTTPException(400, "Token has expired. Please request a new one.")
    user = db.query(User).filter(User.email == record.email).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.password = hash_password(payload.new_password)
    record.used   = True
    db.commit()
    return {"message": "Password reset successfully! You can now login with your new password."}
