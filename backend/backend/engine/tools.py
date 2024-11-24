from backend.engine.function_schemas import *
from langchain.tools import tool
from typing import Any
import json
from datetime import datetime
from backend.config.database import MongoDB
from backend.types import SymptomBase
from backend.engine.utils.sendEmail import send_email
# Symptom logging function

db = MongoDB.connect_to_mongodb()["users"]

@tool("log-symptom-tool", args_schema=LogSymptomSchema, return_direct=True)
def log_symptom(description: str):
    """Log a user-reported symptom or issue into the data store"""
    symptom_time = datetime.now()
    user_query = {"email": "alice@example.com"}
    update_command = {
        "$push": {
            "symptoms": 
                SymptomBase(description=description, date=symptom_time).model_dump()
        }
    }
    db.update_one(user_query, update_command)

@tool("notify-caretaker-tool", args_schema=SendEmailSchema, return_direct=True)
def notify_caretaker(contents: str) -> Any:
    """Evaluates primary caretaker in case of emergency. Only to be used when user reports a high severity or pain level higher than 10"""
    send_email(sender_name="Alice", recipient_name="Doc Name", body=contents)

@tool("calculate-tool", args_schema=CalculateInputsSchema, return_direct=True)
def calculate(expression: str) -> Any:
    """Evaluate a mathematical expression""" 
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": f"Invalid expression: {str(e)}"})
