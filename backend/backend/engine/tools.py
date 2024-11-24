from backend.engine.function_schemas import *
from langchain.tools import tool
from typing import Any
import json
from datetime import datetime
from backend.config.database import MongoDB
from backend.types import SymptomBase
from twilio.rest import Client
import os
from dotenv import load_dotenv
load_dotenv()

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

@tool("reminder-tool", args_schema=ReminderSchema, return_direct=True)
# def reminder(description: str, reminder_times: list, frequency:int ) -> Any:
def reminder(description: str) -> Any:
    """Create a reminder"""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="This is a message sent with CareTakerAI where we take care of you.",
        from_="+19789694707",
        to="+15483337532"
        # scheduleType="fixed",
        # sendAt=datetime(2024, 11, 23, 23, 55, 27),
    )
        

@tool("calculate-tool", args_schema=CalculateInputsSchema, return_direct=True)
def calculate(expression: str) -> Any:
    """Evaluate a mathematical expression""" 
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": f"Invalid expression: {str(e)}"})

@tool("query-date-range-tool", args_schema=QueryDateRange, return_direct=True)
def query_by_name_and_date_range(name: str, start_date:str, end_date:str) -> Any:
    """
    Query all relevant data for a user with the specified name and a date range
    for symptoms, past diagnoses, allergies, medications, and health_conditions.
    """
    try:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = {
            "name": "Alice",
            "$or": [
                {"symptoms.date": {"$gte": start_date, "$lte": end_date}},
                {"past_diagnoses.date": {"$gte": start_date, "$lte": end_date}},
                {"allergies.date": {"$gte": start_date, "$lte": end_date}},
                {"medications.date": {"$gte": start_date, "$lte": end_date}},
            ]
        }

        # Query the database
        result = db.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}

@tool("query-field-tool", args_schema=QueryField, return_direct=True)
def query_by_name_and_field(name:str, field:str) -> Any:
    """
    Query a specific field (e.g., allergies, medications) for a user by name.
    
    :param name: Name of the user
    :param field: Field to query (allergies, medications, etc.)
    :return: MongoDB query results
    """
    try:
        if field not in ["allergies", "medications", "symptoms", "past_diagnoses","health_conditions"]:
            return {"error": "Invalid field specified. Valid fields are: allergies, medications, symptoms, past_diagnoses."}

        query = { "name": "Alice" }

        # Add the specified field to the query
        query[field] = {"$exists": True}

        # Query the database
        result = db.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}
