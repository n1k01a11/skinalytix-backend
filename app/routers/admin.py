import os
import uuid
import shutil
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", response_model=schemas.AdminOut)
def admin_login(credentials: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.AdminUser).filter(models.AdminUser.username == credentials.username).first()
    if not admin or not pwd_context.verify(credentials.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return admin

@router.get("/stats", response_model=schemas.AdminStats)
def get_stats(db: Session = Depends(get_db)):
    total_users = db.query(models.User).count()
    active_users = db.query(models.User).filter(models.User.status == "active").count()
    total_products = db.query(models.Product).count()
    active_products = db.query(models.Product).filter(models.Product.recommendation_status == "active").count()
    week_ago = datetime.utcnow() - timedelta(days=7)
    recent_registrations = db.query(models.User).filter(models.User.created_at >= week_ago).count()
    return schemas.AdminStats(
        total_users=total_users,
        active_users=active_users,
        total_products=total_products,
        active_products=active_products,
        recent_registrations=recent_registrations,
    )

@router.get("/products", response_model=list[schemas.ProductOut])
def list_all_products_admin(db: Session = Depends(get_db)):
    return db.query(models.Product).order_by(models.Product.product_id).all()

@router.post("/products/upload-image")
async def upload_product_image(image: UploadFile = File(...)):
    os.makedirs("static/product_photos", exist_ok=True)
    ext = os.path.splitext(image.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join("static/product_photos", filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    return {"image_url": f"/static/product_photos/{filename}"}

@router.get("/users", response_model=list[schemas.UserAdminOut])
def list_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.created_at.desc()).all()

@router.get("/users/{user_id}", response_model=schemas.UserAdminOut)
def get_user_detail(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=schemas.UserAdminOut)
def update_user(user_id: int, data: schemas.UserAdminUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in data.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.patch("/users/{user_id}/status", response_model=schemas.UserAdminOut)
def toggle_user_status(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "inactive" if user.status == "active" else "active"
    db.commit()
    db.refresh(user)
    return user

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted"}