from fastapi import FastAPI, HTTPException
from backend.config.database import MongoDB
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from contextlib import asynccontextmanager

app = FastAPI()

# Use FastAPI's lifespan for managing the connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB on startup
    app.mongodb = MongoDB.connect_to_mongodb()
    yield
    # Close MongoDB connection on shutdown
    MongoDB.close_mongodb_connection()

app = FastAPI(lifespan=lifespan)

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

@app.post("/register")
async def register_user(user: UserCreate):
    try:
        user_dict = user.model_dump()
        if user.age is not None and user.age < 18:
            raise HTTPException(status_code=400, detail="Age must be 18 or older")

        # Use the MongoDB instance from the app state
        result = app.mongodb.users.insert_one(user_dict)

        return {
            "status": "success",
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
