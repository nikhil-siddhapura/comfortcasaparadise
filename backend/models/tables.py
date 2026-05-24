from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL, Date, Enum, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database.connection import Base


class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    full_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True, nullable=False)
    password      = Column(String(255), nullable=False)
    phone         = Column(String(20))
    bio           = Column(Text)
    profile_image = Column(String(255))
    is_active     = Column(Boolean, default=True)
    created_at    = Column(TIMESTAMP, server_default=func.now())
    bookings      = relationship("Booking",  back_populates="user")
    feedbacks     = relationship("Feedback", back_populates="user")
    contacts      = relationship("Contact",  back_populates="user")


class Category(Base):
    __tablename__ = "categories"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text)
    price       = Column(DECIMAL(10, 2), nullable=False)
    image       = Column(String(255))
    is_active   = Column(Boolean, default=True)
    created_at  = Column(TIMESTAMP, server_default=func.now())
    products    = relationship("Product", back_populates="category", cascade="all, delete")


class Product(Base):
    __tablename__ = "products"
    id              = Column(Integer, primary_key=True, index=True)
    category_id     = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    name            = Column(String(150), nullable=False)
    description     = Column(Text)
    price           = Column(DECIMAL(10, 2), nullable=False)
    total_rooms     = Column(Integer, default=1)
    available_rooms = Column(Integer, default=1)
    image           = Column(String(255))
    is_active       = Column(Boolean, default=True)
    created_at      = Column(TIMESTAMP, server_default=func.now())
    category        = relationship("Category", back_populates="products")
    bookings        = relationship("Booking",  back_populates="product")


class Booking(Base):
    __tablename__ = "bookings"
    id            = Column(Integer, primary_key=True, index=True)
    user_id       = Column(Integer, ForeignKey("users.id",    ondelete="CASCADE"))
    product_id    = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    check_in      = Column(Date, nullable=False)
    check_out     = Column(Date, nullable=False)
    adults        = Column(Integer, nullable=False, default=1)
    children      = Column(Integer, default=0)
    total_price   = Column(DECIMAL(10, 2))
    status        = Column(Enum("pending", "approved", "rejected"), default="pending")
    admin_message = Column(Text)
    created_at    = Column(TIMESTAMP, server_default=func.now())
    user          = relationship("User",    back_populates="bookings")
    product       = relationship("Product", back_populates="bookings")
    feedback      = relationship("Feedback", back_populates="booking", uselist=False)
    services      = relationship("BookingService", back_populates="booking")


class Feedback(Base):
    __tablename__ = "feedback"
    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id",    ondelete="CASCADE"))
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"))
    rating     = Column(Integer, nullable=False)
    comment    = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user       = relationship("User",    back_populates="feedbacks")
    booking    = relationship("Booking", back_populates="feedback")


class Contact(Base):
    __tablename__ = "contacts"
    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    name        = Column(String(100), nullable=False)
    email       = Column(String(100), nullable=False)
    subject     = Column(String(200))
    message     = Column(Text, nullable=False)
    admin_reply = Column(Text)
    is_read     = Column(Boolean, default=False)
    created_at  = Column(TIMESTAMP, server_default=func.now())
    user        = relationship("User", back_populates="contacts")


class Service(Base):
    __tablename__ = "services"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    description = Column(Text)
    price       = Column(DECIMAL(10, 2), nullable=False)
    image       = Column(String(255))
    is_active   = Column(Boolean, default=True)
    created_at  = Column(TIMESTAMP, server_default=func.now())
    bookings    = relationship("BookingService", back_populates="service")


class BookingService(Base):
    __tablename__ = "booking_services"
    id         = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"))
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"))
    booking    = relationship("Booking", back_populates="services")
    service    = relationship("Service", back_populates="bookings")


class PasswordReset(Base):
    __tablename__ = "password_resets"
    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(100), nullable=False)
    token      = Column(String(255), nullable=False)
    expires_at = Column(TIMESTAMP, nullable=False)
    used       = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
