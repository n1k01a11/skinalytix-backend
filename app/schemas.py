from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    age: int
    sex: Optional[str] = None
    
class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    user_id: int
    full_name: str
    email: str
    age: int
    sex: Optional[str]

    class Config:
        from_attributes = True

class ConsultationCreate(BaseModel):
    user_id: int
    analysis_id: Optional[int] = None
    responses: Dict[str, Any]   # matches the Flutter `answers` map directly
class ConsultationOut(BaseModel):
    consultation_id: int
    user_id: int
    analysis_id: Optional[int]
    responses: Dict[str, Any]

    class Config:
        from_attributes = True
        
class SkinAnalysisCreate(BaseModel):
    user_id: int
    image_path: str
    ai_detected_concerns: List[str]

class ProductCreate(BaseModel):
    brand: str
    product_name: str
    category: str
    skin_types: Optional[List[str]] = []
    skin_concerns: Optional[List[str]] = []
    key_ingredients: Optional[List[str]] = []
    usage_instructions: Optional[str] = None
    time_of_use: Optional[List[str]] = []
    selection_notes: Optional[str] = None
    ingredient_overlap_group: Optional[str] = None
    validation_status: Optional[str] = "Dermatologist-reviewed"
    recommendation_status: Optional[str] = "active"
    image_url: Optional[str] = None


class ProductOut(BaseModel):
    product_id: int
    brand: str
    product_name: str
    category: str
    skin_types: Optional[List[str]]
    skin_concerns: Optional[List[str]]
    key_ingredients: Optional[List[str]]
    usage_instructions: Optional[str]
    time_of_use: Optional[List[str]]
    selection_notes: Optional[str]
    ingredient_overlap_group: Optional[str]
    validation_status: str
    recommendation_status: str
    image_url: Optional[str]

    class Config:
        from_attributes = True

class SkinAnalysisOut(BaseModel):
    analysis_id: int
    user_id: int
    image_path: str
    ai_detected_concerns: List[str]

    class Config:
        from_attributes = True

class SkinProfileRequest(BaseModel):
    user_id: int
    analysis_id: int
    consultation_id: int

class ProductBrief(BaseModel):
    product_id: int
    brand: str
    product_name: str
    category: str
    time_of_use: Optional[List[str]]
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class SkinProfileResult(BaseModel):
    profile_id: int
    skin_type: Optional[str]
    concerns: Optional[List[str]]
    sensitivity: Optional[str]
    sun_exposure: Optional[str]
    primary_goal: Optional[str]
    severity: Optional[str]
    outcome: str   # "recommendation" or "referral"
    referral_reason: Optional[str] = None
    recommended_products: Optional[List[ProductBrief]] = None
    routine_explanation: Optional[str] = None

class HistoryEntry(BaseModel):
    profile_id: int
    created_at: str
    skin_type: Optional[str]
    concerns: Optional[List[str]]
    severity: Optional[str]
    outcome: str  # "recommendation" or "referral"

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminOut(BaseModel):
    admin_id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class UserAdminOut(BaseModel):
    user_id: int
    full_name: str
    email: str
    age: int
    sex: Optional[str]
    status: str
    phone: Optional[str]
    occupation: Optional[str]
    location: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class UserAdminUpdate(BaseModel):
    full_name: str
    email: str
    age: int
    sex: Optional[str] = None
    phone: Optional[str] = None
    occupation: Optional[str] = None
    location: Optional[str] = None

class AdminStats(BaseModel):
    total_users: int
    active_users: int
    total_products: int
    active_products: int
    recent_registrations: int