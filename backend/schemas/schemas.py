from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    username: str
    password: str

class ForgotPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    bio: Optional[str]
    profile_image: Optional[str]
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None

# ── Category ──────────────────────────────────────────────────
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image: Optional[str]
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# ── Product ───────────────────────────────────────────────────
class ProductCreate(BaseModel):
    category_id: int
    name: str
    description: Optional[str] = None
    price: float
    total_rooms: int = 1
    available_rooms: int = 1

class ProductUpdate(BaseModel):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    total_rooms: Optional[int] = None
    available_rooms: Optional[int] = None
    is_active: Optional[bool] = None

class ProductOut(BaseModel):
    id: int
    category_id: int
    name: str
    description: Optional[str]
    price: float
    total_rooms: int
    available_rooms: int
    image: Optional[str]
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# ── Booking ───────────────────────────────────────────────────
class BookingStatusEnum(str, Enum):
    pending  = "pending"
    approved = "approved"
    rejected = "rejected"

class BookingCreate(BaseModel):
    product_id: int
    check_in: date
    check_out: date
    adults: int
    children: int = 0
    service_ids: Optional[List[int]] = []

    @field_validator("adults")
    @classmethod
    def min_adults(cls, v):
        if v < 1:
            raise ValueError("At least 1 adult required")
        return v

    @field_validator("check_out")
    @classmethod
    def checkout_after_checkin(cls, v, info):
        if "check_in" in info.data and v <= info.data["check_in"]:
            raise ValueError("Check-out must be after check-in")
        return v

class BookingUpdate(BaseModel):
    status: BookingStatusEnum
    admin_message: Optional[str] = None

class BookingOut(BaseModel):
    id: int
    user_id: int
    product_id: int
    check_in: date
    check_out: date
    adults: int
    children: int
    total_price: Optional[float]
    status: str
    admin_message: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# ── Feedback ──────────────────────────────────────────────────
class FeedbackCreate(BaseModel):
    booking_id: int
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def valid_rating(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v

class FeedbackOut(BaseModel):
    id: int
    user_id: int
    booking_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True

# ── Contact ───────────────────────────────────────────────────
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = None
    message: str

class ContactReply(BaseModel):
    admin_reply: str

class ContactOut(BaseModel):
    id: int
    user_id: Optional[int]
    name: str
    email: str
    subject: Optional[str]
    message: str
    admin_reply: Optional[str]
    is_read: bool
    created_at: datetime
    class Config:
        from_attributes = True

# ── Service ───────────────────────────────────────────────────
class ServiceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_active: Optional[bool] = None

class ServiceOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    image: Optional[str]
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True
