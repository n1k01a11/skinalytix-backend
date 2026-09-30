from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.post("/", response_model=schemas.ProductOut)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/", response_model=list[schemas.ProductOut])
def list_products(
    category: Optional[str] = None,
    time_of_use: Optional[str] = None,   # filter e.g. ?time_of_use=AM
    db: Session = Depends(get_db),
):
    query = db.query(models.Product).filter(models.Product.recommendation_status == "active")
    if category:
        query = query.filter(models.Product.category == category)
    if time_of_use:
        query = query.filter(models.Product.time_of_use.contains([time_of_use]))
    return query.all()

@router.get("/{product_id}", response_model=schemas.ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=schemas.ProductOut)
def update_product(product_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.dict().items():
        setattr(existing, key, value)
    db.commit()
    db.refresh(existing)
    return existing

@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    existing = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(existing)
    db.commit()
    return {"message": "Product deleted"}