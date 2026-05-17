from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os, uuid

from database.connection import get_db
from models.tables import Category
from schemas.schemas import CategoryOut, CategoryUpdate
from routers.dependencies import require_admin

router     = APIRouter(prefix="/categories", tags=["Categories"])
UPLOAD_DIR = "uploads/categories"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Public: only active categories
@router.get("/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).filter(Category.is_active == True).all()

# Admin: ALL categories (active + inactive)
@router.get("/admin/all", response_model=List[CategoryOut])
def get_all_categories_admin(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Category).all()

@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    return cat

# Admin: Create category with optional image
@router.post("/", response_model=CategoryOut, status_code=201)
def create_category(
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    image_path = None
    if image and image.filename:
        ext        = image.filename.rsplit(".", 1)[-1].lower()
        filename   = f"{uuid.uuid4()}.{ext}"
        image_path = f"{UPLOAD_DIR}/{filename}"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    cat = Category(name=name, description=description, price=price, image=image_path)
    db.add(cat); db.commit(); db.refresh(cat)
    return cat

# Admin: Update category (name, desc, price, status)
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(cat, field, value)
    db.commit(); db.refresh(cat)
    return cat

# Admin: Update category image separately
@router.put("/{category_id}/image", response_model=CategoryOut)
def update_category_image(
    category_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    ext        = image.filename.rsplit(".", 1)[-1].lower()
    filename   = f"{uuid.uuid4()}.{ext}"
    image_path = f"{UPLOAD_DIR}/{filename}"
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    cat.image = image_path
    db.commit(); db.refresh(cat)
    return cat

# Admin: Delete category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    cat = db.query(Category).filter(Category.id == category_id).first()
    if not cat:
        raise HTTPException(404, "Category not found")
    db.delete(cat); db.commit()
    return {"message": "Category deleted successfully"}
