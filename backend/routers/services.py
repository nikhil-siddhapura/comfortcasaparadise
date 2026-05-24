from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil, os, uuid

from database.connection import get_db
from models.tables import Service
from schemas.schemas import ServiceOut, ServiceUpdate
from routers.dependencies import require_admin

router     = APIRouter(prefix="/services", tags=["Services"])
UPLOAD_DIR = "uploads/services"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Public: active services
@router.get("/", response_model=List[ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return db.query(Service).filter(Service.is_active == True).all()

# Admin: ALL services
@router.get("/admin/all", response_model=List[ServiceOut])
def get_all_services_admin(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Service).all()

# Admin: Create service with optional image
@router.post("/", response_model=ServiceOut, status_code=201)
def create_service(
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

    svc = Service(name=name, description=description, price=price, image=image_path)
    db.add(svc); db.commit(); db.refresh(svc)
    return svc

# Admin: Update service details
@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    payload: ServiceUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    svc = db.query(Service).filter(Service.id == service_id).first()
    if not svc:
        raise HTTPException(404, "Service not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(svc, field, value)
    db.commit(); db.refresh(svc)
    return svc

# Admin: Update service image separately
@router.put("/{service_id}/image", response_model=ServiceOut)
def update_service_image(
    service_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    svc = db.query(Service).filter(Service.id == service_id).first()
    if not svc:
        raise HTTPException(404, "Service not found")
    ext        = image.filename.rsplit(".", 1)[-1].lower()
    filename   = f"{uuid.uuid4()}.{ext}"
    image_path = f"{UPLOAD_DIR}/{filename}"
    with open(image_path, "wb") as f:
        shutil.copyfileobj(image.file, f)
    svc.image = image_path
    db.commit(); db.refresh(svc)
    return svc

# Admin: Delete service
@router.delete("/{service_id}")
def delete_service(service_id: int, db: Session = Depends(get_db), admin=Depends(require_admin)):
    svc = db.query(Service).filter(Service.id == service_id).first()
    if not svc:
        raise HTTPException(404, "Service not found")
    db.delete(svc); db.commit()
    return {"message": "Service deleted successfully"}
