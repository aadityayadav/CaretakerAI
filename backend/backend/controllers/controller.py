import fastapi
from fastapi import HTTPException
from pydantic import BaseModel
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Use your existing MongoDB connection
uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["client_db"]

app = fastapi.FastAPI()

# Create a user model matching your MongoDB schema
class UserCreate(BaseModel):
    name: str
    email: str
    age: int
    gender: str | None = None
    weight: float | None = None
    height: float | None = None

@app.post("/users/register")
async def register_user(user: UserCreate):
    try:
        # Check if user already exists
        if db.users.find_one({"email": user.email}):
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create user document
        user_data = user.model_dump()
        # Initialize empty arrays for the required schema fields
        user_data["symptoms"] = []
        user_data["past_diagnoses"] = []
        user_data["allergies"] = []
        user_data["medications"] = []

        result = db.users.insert_one(user_data)

        return {
            "message": "User registered successfully",
            "user_id": str(result.inserted_id)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
