from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/skin-profiles", tags=["skin_profiles"])

# Keywords used to match your products' `category` values to routine steps.
# This tolerates the different labels in your 30-product list
# (e.g. "Serum", "Essence", "Serum/Sunscreen", "Gel Moisturizer").
CATEGORY_KEYWORDS = {
    "Cleanser": ["Cleanser"],
    "Serum": ["Serum", "Essence"],
    "Sunscreen": ["Sunscreen"],
    "Moisturizer": ["Moisturizer"],
}


def match_best_product(db: Session, keywords: list[str], skin_type: str | None, concerns: list[str]):
    """Real matching against the products table — not hardcoded.
    Scores each candidate by skin-type match + overlapping concerns,
    and picks the highest scorer (falls back to the first candidate
    in that category if nothing scores above 0)."""
    all_active = db.query(models.Product).filter(models.Product.recommendation_status == "active").all()
    candidates = [p for p in all_active if any(kw.lower() in p.category.lower() for kw in keywords)]

    best, best_score = None, -1
    for p in candidates:
        score = 0
        if skin_type and p.skin_types and skin_type in p.skin_types:
            score += 2
        if concerns and p.skin_concerns:
            score += len(set(concerns) & set(p.skin_concerns))
        if score > best_score:
            best_score, best = score, p

    if best_score > 0:
        return best
    return candidates[0] if candidates else None


@router.post("/", response_model=schemas.SkinProfileResult)
def create_skin_profile(data: schemas.SkinProfileRequest, db: Session = Depends(get_db)):
    analysis = db.query(models.SkinAnalysis).filter(
        models.SkinAnalysis.analysis_id == data.analysis_id).first()
    consultation = db.query(models.Consultation).filter(
        models.Consultation.consultation_id == data.consultation_id).first()

    if not analysis or not consultation:
        raise HTTPException(status_code=404, detail="Analysis or consultation not found")

    responses = consultation.responses
    skin_type = responses.get("skinType") or responses.get("skinChar")
    consultation_concerns = responses.get("concerns", []) or []
    ai_concerns = analysis.ai_detected_concerns or []
    combined_concerns = list(set(consultation_concerns + ai_concerns))

    symptoms = responses.get("symptoms", []) or []
    has_real_symptoms = any(s != "None" for s in symptoms)
    sensitivity = "Sensitive / reactive" if has_real_symptoms else "No reported symptoms"

    severity = responses.get("severity")

    profile = models.SkinProfile(
        user_id=data.user_id,
        analysis_id=data.analysis_id,
        consultation_id=data.consultation_id,
        skin_type=skin_type,
        concerns=combined_concerns,
        sensitivity=sensitivity,
        sun_exposure=responses.get("sunExposure"),
        primary_goal=responses.get("goal"),
        severity=severity,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)

    # ---- Referral screening happens BEFORE any product matching ----
    if severity == "Severe":
        referral = models.Referral(
            user_id=data.user_id,
            profile_id=profile.profile_id,
            reason="Reported severity is severe and may require professional dermatological evaluation.",
        )
        db.add(referral)
        db.commit()

        return schemas.SkinProfileResult(
            profile_id=profile.profile_id,
            skin_type=profile.skin_type,
            concerns=profile.concerns,
            sensitivity=profile.sensitivity,
            sun_exposure=profile.sun_exposure,
            primary_goal=profile.primary_goal,
            severity=profile.severity,
            outcome="referral",
            referral_reason=referral.reason,
        )

    # ---- OTC recommendation: real query against the 30-product table ----
    selected_products = []
    for keywords in CATEGORY_KEYWORDS.values():
        product = match_best_product(db, keywords, skin_type, combined_concerns)
        if product:
            selected_products.append(product)

    product_ids = [p.product_id for p in selected_products]
    goal_text = f" This may help support your goal of {profile.primary_goal.lower()}." if profile.primary_goal else ""
    explanation = (
        "These products were selected because they match your identified skin type and concerns."
        + goal_text
    )

    recommendation = models.Recommendation(
        user_id=data.user_id,
        profile_id=profile.profile_id,
        product_ids=product_ids,
        routine_explanation=explanation,
    )
    db.add(recommendation)
    db.commit()

    return schemas.SkinProfileResult(
        profile_id=profile.profile_id,
        skin_type=profile.skin_type,
        concerns=profile.concerns,
        sensitivity=profile.sensitivity,
        sun_exposure=profile.sun_exposure,
        primary_goal=profile.primary_goal,
        severity=profile.severity,
        outcome="recommendation",
        recommended_products=[schemas.ProductBrief.from_orm(p) for p in selected_products],
        routine_explanation=explanation,
    )

@router.get("/user/{user_id}", response_model=list[schemas.HistoryEntry])
def get_user_history(user_id: int, db: Session = Depends(get_db)):
    profiles = (
        db.query(models.SkinProfile)
        .filter(models.SkinProfile.user_id == user_id)
        .order_by(models.SkinProfile.created_at.desc())
        .all()
    )

    results = []
    for p in profiles:
        referral = db.query(models.Referral).filter(models.Referral.profile_id == p.profile_id).first()
        outcome = "referral" if referral else "recommendation"

        results.append(schemas.HistoryEntry(
            profile_id=p.profile_id,
            created_at=p.created_at.strftime("%B %Y"),
            skin_type=p.skin_type,
            concerns=p.concerns,
            severity=p.severity,
            outcome=outcome,
        ))

    return results

@router.get("/{profile_id}", response_model=schemas.SkinProfileResult)
def get_skin_profile_detail(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(models.SkinProfile).filter(models.SkinProfile.profile_id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    referral = db.query(models.Referral).filter(models.Referral.profile_id == profile_id).first()
    if referral:
        return schemas.SkinProfileResult(
            profile_id=profile.profile_id,
            skin_type=profile.skin_type,
            concerns=profile.concerns,
            sensitivity=profile.sensitivity,
            sun_exposure=profile.sun_exposure,
            primary_goal=profile.primary_goal,
            severity=profile.severity,
            outcome="referral",
            referral_reason=referral.reason,
        )

    recommendation = db.query(models.Recommendation).filter(
        models.Recommendation.profile_id == profile_id).first()

    products = []
    explanation = None
    if recommendation:
        product_ids = recommendation.product_ids or []
        products = db.query(models.Product).filter(models.Product.product_id.in_(product_ids)).all()
        explanation = recommendation.routine_explanation

    return schemas.SkinProfileResult(
        profile_id=profile.profile_id,
        skin_type=profile.skin_type,
        concerns=profile.concerns,
        sensitivity=profile.sensitivity,
        sun_exposure=profile.sun_exposure,
        primary_goal=profile.primary_goal,
        severity=profile.severity,
        outcome="recommendation",
        recommended_products=[schemas.ProductBrief.from_orm(p) for p in products],
        routine_explanation=explanation,
    )