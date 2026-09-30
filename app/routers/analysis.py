import os
import uuid
import json
import shutil
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/analysis", tags=["analysis"])

UPLOAD_DIR = "uploads/skin_photos"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.SkinAnalysisOut)
def create_analysis(
    user_id: int = Form(...),
    ai_detected_concerns: str = Form(...),  # JSON string, e.g. '["Acne","Dark spots"]'
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    ext = os.path.splitext(image.filename)[1] or ".jpg"
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    try:
        concerns_list = json.loads(ai_detected_concerns)
    except json.JSONDecodeError:
        concerns_list = [ai_detected_concerns]

    new_analysis = models.SkinAnalysis(
        user_id=user_id,
        image_path=filepath,
        ai_detected_concerns=concerns_list,
    )
    db.add(new_analysis)
    db.commit()
    db.refresh(new_analysis)
    return new_analysis

@router.get("/user/{user_id}", response_model=list[schemas.SkinAnalysisOut])
def get_user_analyses(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.SkinAnalysis)
        .filter(models.SkinAnalysis.user_id == user_id)
        .order_by(models.SkinAnalysis.analyzed_at.desc())
        .all()
    )