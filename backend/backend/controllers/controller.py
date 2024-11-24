from fastapi import FastAPI, HTTPException
from backend.config.database import MongoDB
from contextlib import asynccontextmanager
from backend.types import UserCreate, QueryBody
from backend.engine.agents import create_user_agent, create_doctor_agent
from backend.engine.llm import get_model
from fastapi.middleware.cors import CORSMiddleware
from backend.engine.chain import check_discrepancies

app = FastAPI()
llm = get_model()
agent = create_user_agent(llm)
doctor_agent = create_doctor_agent(llm)

# Use FastAPI's lifespan for managing the connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to MongoDB on startup
    app.mongodb = MongoDB.connect_to_mongodb()
    yield
    # Close MongoDB connection on shutdown
    MongoDB.close_mongodb_connection()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/user/query")
async def user_query(query: QueryBody):
    try:
        history = []
        if query.history:
            history = [q.model_dump() for q in query.history]
        result = agent.invoke({
            "input": query.query,
            "chat_history": history if history else []
        })

        return {
            "status": "success",
            "result": result['output']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/doctor/query")
async def doctor_query(query: QueryBody):
    try:
        history = []
        if query.history:
            history = [q.model_dump() for q in query.history]
        result = doctor_agent.invoke({
            "input": query.query,
            "chat_history": history if history else []
        });

        return {
            "status": "success",
            "result": result['output']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/doctor/flags")
async def raise_flags(name: str):
    try:
        result = check_discrepancies(llm)
        return {
            "status": "success",
            "result": result['output']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
