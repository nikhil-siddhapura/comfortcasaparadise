from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os, uuid

from database.connection import get_db
from models.tables import Product
from schemas.schemas import ProductOut, ProductUpdate
from routers.dependencies import require_admin

router     = APIRouter(prefix="/products", tags=["Products"])
UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Public: active products (optionally filtered by category)
@router.get("/", response_model=List[ProductOut])
def get_products(category_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(Product).filter(Product.is_active == True)
    if category_id:
        q = q.filter(Product.category_id == category_id)
    return q.all()

# Admin: ALL products
@router.get("/admin/all", response_model=List[ProductOut])
def get_all_products_admin(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Product).all()

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Product not found")
    return p

# Admin: Create product with optional image
@router.post("/", response_model=ProductOut, status_code=201)
def create_product(
    category_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(None),
    price: float = Form(...),
    total_rooms: int = Form(1),
    available_rooms: int = Form(1),
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

    p = Product(category_id=category_id, name=name, description=description,
                price=price, total_rooms=total_rooms,
                available_rooms=available_rooms, image=image_path)
    db.add(p); db.commit(); db.refresh(p)
    return p

# Admin: Update product details
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Product not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(p, field, value)
    db.commit(); db.refresh(p)
    return p

# Admin: Update product image separately
@router.put("/{product_id}/image", response_model=ProductOut)
def update_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Product not found")
    ext        = image.filename.rsplit(".", 1)[-1].lower()
    filename   = f"{uuid.uuid4()}.{ext}"
    image_path = f"{UPLOAD_DIR}/{filename}"
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    p.image = image_path
    db.commit(); db.refresh(p)
    return p

# Admin: Delete product
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(404, "Product not found")
    db.delete(p); db.commit()
    return {"message": "Product deleted successfully"}
