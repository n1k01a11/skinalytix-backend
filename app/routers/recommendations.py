from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"]
)


@router.post("/")
def create_recommendation(
    recommendation: dict,
    db: Session = Depends(get_db)
):
    # Check if the user exists
    user = db.query(models.User).filter(
        models.User.user_id == recommendation.get("user_id")
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Check if the skin profile exists
    profile = db.query(models.SkinProfile).filter(
        models.SkinProfile.profile_id == recommendation.get("profile_id")
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Skin profile not found"
        )

    new_recommendation = models.Recommendation(
        user_id=recommendation.get("user_id"),
        profile_id=recommendation.get("profile_id"),
        product_ids=recommendation.get("product_ids"),
        routine_explanation=recommendation.get("routine_explanation")
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return {
        "message": "Recommendation saved successfully",
        "recommendation_id": new_recommendation.recommendation_id
    }


@router.get("/")
def get_recommendations(
    db: Session = Depends(get_db)
):
    recommendations = db.query(
        models.Recommendation
    ).all()

    return recommendations