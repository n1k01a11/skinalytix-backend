from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, nullable=False)
    sex = Column(String(30))
    created_at = Column(TIMESTAMP, server_default=func.now())

class SkinAnalysis(Base):
    __tablename__ = "skin_analyses"
    analysis_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    image_path = Column(Text)
    ai_detected_concerns = Column(JSONB)
    analyzed_at = Column(TIMESTAMP, server_default=func.now())

class Consultation(Base):
    __tablename__ = "consultations"
    consultation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    analysis_id = Column(Integer, ForeignKey("skin_analyses.analysis_id", ondelete="SET NULL"))
    responses = Column(JSONB, nullable=False)
    submitted_at = Column(TIMESTAMP, server_default=func.now())

class SkinProfile(Base):
    __tablename__ = "skin_profiles"
    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    analysis_id = Column(Integer, ForeignKey("skin_analyses.analysis_id", ondelete="SET NULL"))
    consultation_id = Column(Integer, ForeignKey("consultations.consultation_id", ondelete="SET NULL"))
    skin_type = Column(String(50))
    concerns = Column(JSONB)
    sensitivity = Column(String(100))
    sun_exposure = Column(String(50))
    primary_goal = Column(String(100))
    severity = Column(String(20))
    created_at = Column(TIMESTAMP, server_default=func.now())

class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(100), nullable=False)
    product_name = Column(String(150), nullable=False)
    category = Column(String(50), nullable=False)
    skin_types = Column(JSONB)
    skin_concerns = Column(JSONB)
    key_ingredients = Column(JSONB)
    usage_instructions = Column(Text)
    time_of_use = Column(JSONB)  # e.g. ["AM"], ["PM"], or ["AM", "PM"]
    selection_notes = Column(Text)  # why one product may be preferred over a similar one
    ingredient_overlap_group = Column(String(50))  # groups products sharing key ingredients
    validation_status = Column(String(30), default="Dermatologist-reviewed")
    recommendation_status = Column(String(20), default="active")
    created_at = Column(TIMESTAMP, server_default=func.now())
    image_url = Column(Text)

class Recommendation(Base):
    __tablename__ = "recommendations"
    recommendation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    profile_id = Column(Integer, ForeignKey("skin_profiles.profile_id", ondelete="SET NULL"))
    product_ids = Column(JSONB)
    routine_explanation = Column(Text)
    generated_at = Column(TIMESTAMP, server_default=func.now())

class Referral(Base):
    __tablename__ = "referrals"
    referral_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"))
    profile_id = Column(Integer, ForeignKey("skin_profiles.profile_id", ondelete="SET NULL"))
    reason = Column(Text)
    referred_at = Column(TIMESTAMP, server_default=func.now())