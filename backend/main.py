from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from database.connection import Base, engine
from routers import (
    auth,
    categories,
    products,
    bookings,
    feedback,
    contacts,
    services,
    users,
)

# Auto-create all DB tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resort Management System API",
    version="1.0.0",
    description="Full-stack Resort Management System — FastAPI + MySQL",
)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. માઉન્ટિંગ સેટિંગ્સ (સ્ટાટીક ફાઇલો માટે)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# આખી ફ્રન્ટએન્ડ ડિરેક્ટરી માઉન્ટ કરી દઈએ જેથી css, js, images બધું એકસાથે લોડ થઈ જાય
app.mount("/css", StaticFiles(directory="../frontend/css"), name="css")
app.mount("/js", StaticFiles(directory="../frontend/js"), name="js")

# 2. રજીસ્ટર ઓલ રાઉટર્સ (API Endpoints)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(bookings.router)
app.include_router(feedback.router)
app.include_router(contacts.router)
app.include_router(services.router)
app.include_router(users.router)


# 3. ફ્રન્ટએન્ડ પેજીસના રાઉટ્સ
@app.get("/")
def root():
    return FileResponse("../frontend/index.html")


@app.get("/login.html")
def login_page():
    return FileResponse("../frontend/login.html")


@app.get("/register.html")
def register_page():
    return FileResponse("../frontend/register.html")


@app.get("/booking.html")
def booking_page():
    return FileResponse("../frontend/booking.html")


@app.get("/profile.html")
def profile_page():
    return FileResponse("../frontend/profile.html")


@app.get("/products.html")
def products_page():
    return FileResponse("../frontend/products.html")


@app.get("/forgot-password.html")
def forgot_page():
    return FileResponse("../frontend/forgot-password.html")


# એડમિન પેજીસના રાઉટ્સ
@app.get("/admin/dashboard.html")
def admin_dashboard():
    return FileResponse("../frontend/admin/dashboard.html")


@app.get("/admin/categories.html")
def admin_categories():
    return FileResponse("../frontend/admin/categories.html")


@app.get("/admin/products.html")
def admin_products():
    return FileResponse("../frontend/admin/products.html")


@app.get("/admin/bookings.html")
def admin_bookings():
    return FileResponse("../frontend/admin/bookings.html")


@app.get("/admin/users.html")
def admin_users():
    return FileResponse("../frontend/admin/users.html")


@app.get("/admin/contacts.html")
def admin_contacts():
    return FileResponse("../frontend/admin/contacts.html")


@app.get("/admin/services.html")
def admin_services():
    return FileResponse("../frontend/admin/services.html")
