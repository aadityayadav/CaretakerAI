from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Pydantic models for request validation
class SymptomBase(BaseModel):
    description: str
    date: datetime

class DiagnosisBase(BaseModel):
    name: str
    description: Optional[str] = None
    doctor_name: Optional[str] = None
    date: datetime

class AllergyBase(BaseModel):
    name: str
    date: datetime

class MedicationBase(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None

class HealthCondition(BaseModel):
    name: str
    date: datetime

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None
    gender: Optional[str] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    symptoms: Optional[List[SymptomBase]] = None
    past_diagnoses: Optional[List[DiagnosisBase]] = None
    allergies: Optional[List[AllergyBase]] = None
    medications: Optional[List[MedicationBase]] = None
    health_conditions: Optional[List[HealthCondition]] = None

class HistoryModel(BaseModel):
    role: str
    content: str

class QueryBody(BaseModel):
    query: str
    summarize: Optional[bool] = False
    history: Optional[List[HistoryModel]] = None
