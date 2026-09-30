from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/consultations", tags=["consultations"])

@router.post("/", response_model=schemas.ConsultationOut)
def submit_consultation(data: schemas.ConsultationCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_consultation = models.Consultation(
        user_id=data.user_id,
        analysis_id=data.analysis_id,
        responses=data.responses,
    )
    db.add(new_consultation)
    db.commit()
    db.refresh(new_consultation)
    return new_consultation

@router.get("/user/{user_id}", response_model=list[schemas.ConsultationOut])
def get_user_consultations(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Consultation)
        .filter(models.Consultation.user_id == user_id)
        .order_by(models.Consultation.submitted_at.desc())
        .all()
    )