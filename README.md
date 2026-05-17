# 🏨 Royal Resort — Management System

**Tech Stack:** FastAPI (Python) + MySQL + HTML/CSS/JavaScript

---

## ⚡ Quick Start (3 Steps)

### Step 1 — Setup Database

```bash
mysql -u root -p < resort_db.sql
```

Then open `backend/.env` and set your MySQL password:

```
DB_PASSWORD=your_actual_password
```

### Step 2 — Run Backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

✅ API running at: http://localhost:8000
📄 Swagger docs: http://localhost:8000/docs

### Step 3 — Open Frontend

Open `frontend/index.html` with **VS Code Live Server**
_(Right-click → Open with Live Server)_

Or use Python:

```bash
cd frontend
python -m http.server 5500
```

✅ Frontend at: http://localhost:5500

---

## 🔐 Login Credentials

| Role  | Username/Email | Password |
| ----- | -------------- | -------- |
| Admin | admin          | admin123 |
| User  | Register yours | 6+ chars |

---

## ✅ Features Checklist

### Admin

- [x] Login with username/password
- [x] Dashboard with stats
- [x] Category — Add, Edit (with image), Update, Delete
- [x] Product — Add, Edit (with image), Update, Delete
- [x] Service — Add, Edit (with image), Update, Delete
- [x] Bookings — View all, Filter by status, Approve/Reject, Send message
- [x] Users — View all registered users
- [x] Messages — View contact messages, Reply to users

### User

- [x] Register, Login, Logout
- [x] Forgot Password (token-based reset)
- [x] Edit profile, upload avatar
- [x] Browse categories and products
- [x] Book a room (min 3 persons, select dates, add services)
- [x] View my bookings with status and admin message
- [x] Leave feedback/review on approved bookings
- [x] Send contact message to admin

### Visitor

- [x] View homepage with categories and products
- [x] Filter rooms by category
- [x] View services
- [x] View guest reviews
- [x] Send contact message

---

## 📁 Project Structure

```
resort_management_system/
├── resort_db.sql              ← Run this first
├── README.md
├── backend/
│   ├── .env                   ← Set your DB password here
│   ├── main.py
│   ├── requirements.txt
│   ├── database/connection.py
│   ├── models/tables.py
│   ├── schemas/schemas.py
│   └── routers/
│       ├── auth.py            ← Register, Login, Forgot Password
│       ├── categories.py      ← Full CRUD + image + admin/all
│       ├── products.py        ← Full CRUD + image + admin/all
│       ├── bookings.py        ← Create, Approve/Reject
│       ├── feedback.py        ← Submit and view reviews
│       ├── contacts.py        ← Send message, admin reply
│       ├── services.py        ← Full CRUD + image + admin/all
│       ├── users.py           ← Profile, avatar upload
│       └── dependencies.py   ← JWT auth guards
└── frontend/
    ├── index.html             ← Homepage
    ├── login.html             ← User + Admin login
    ├── register.html          ← Register
    ├── forgot-password.html   ← Password reset
    ├── products.html          ← All rooms listing
    ├── booking.html           ← Book a room + My bookings
    ├── profile.html           ← Edit profile + avatar
    ├── css/
    │   ├── style.css
    │   ├── auth.css
    │   └── admin.css
    ├── js/
    │   ├── api.js             ← All API calls
    │   ├── auth.js
    │   ├── home.js
    │   └── booking.js
    ├── images/
    │   └── hero-bg.svg        ← Resort background image
    └── admin/
        ├── dashboard.html
        ├── categories.html    ← Add/Edit/Update/Delete + image
        ├── products.html      ← Add/Edit/Update/Delete + image
        ├── bookings.html      ← Approve/Reject + filter tabs
        ├── users.html
        ├── contacts.html      ← View + Reply
        └── services.html      ← Add/Edit/Update/Delete + image
```

---

## 🔑 Forgot Password Flow

1. Go to `forgot-password.html`
2. Enter registered email → Click **Get Reset Token**
3. Token appears on screen — **copy it**
4. Paste in "Reset Token" field below
5. Enter new password → Click **Reset Password**
6. Login with new password ✅

---

## 🖼️ Image Upload

Images can be uploaded when:

- **Adding** a category / product / service
- **Editing** a category / product / service (separate image field)
- **Profile** avatar upload

Images are stored in `backend/uploads/` and served at `http://localhost:8000/uploads/...`

---

## 🛠️ Common Errors

| Error                      | Fix                                   |
| -------------------------- | ------------------------------------- |
| `Access denied` MySQL      | Update `DB_PASSWORD` in `.env`        |
| `Module not found`         | Run `pip install -r requirements.txt` |
| CORS error in browser      | Make sure backend runs on port 8000   |
| `uvicorn not found`        | Activate virtual environment first    |
| Images not showing         | Make sure backend is running          |
| `422 Unprocessable Entity` | Check Swagger docs at `/docs`         |

---

## 🌐 All URLs

| URL                                        | Description          |
| ------------------------------------------ | -------------------- |
| http://localhost:8000                      | Backend health check |
| http://localhost:8000/docs                 | Swagger API explorer |
| http://localhost:5500/index.html           | Homepage             |
| http://localhost:5500/login.html           | Login page           |
| http://localhost:5500/admin/dashboard.html | Admin panel          |
