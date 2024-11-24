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
from backend.engine.utils.sendEmail import send_email
# Symptom logging function


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
    body = f"""
    {description}
    
    This is a message sent with CareTakerAI where we take care of you.
    """
    message = client.messages.create(
        body=body,
        from_="+19789694707",
        to="+15483337532"
        # scheduleType="fixed",
        # sendAt=datetime(2024, 11, 23, 23, 55, 27),
    )
        

@tool("notify-caretaker-tool", args_schema=SendEmailSchema, return_direct=True)
def notify_caretaker(contents: str) -> Any:
    """Evaluates primary caretaker in case of emergency. Only to be used when user reports a high severity or pain level higher than 10"""
    send_email(sender_name="Alice", recipient_name="Doc Name", body=contents)


# @tool("calculate-tool", args_schema=CalculateInputsSchema, return_direct=True)
# def calculate(expression: str) -> Any:
#     """Evaluate a mathematical expression""" 
#     try:
#         result = eval(expression)
#         return json.dumps({"result": result})
#     except Exception as e:
#         return json.dumps({"error": f"Invalid expression: {str(e)}"})

# @tool("query-date-range-tool", args_schema=QueryDateRange, return_direct=True)
# def query_by_name_and_date_range(name: str, start_date:str, end_date:str) -> Any:
#     """
#     Query all relevant data for a user with the specified name and a date range
#     for symptoms, past diagnoses, allergies, medications, and health_conditions.
#     """
#     try:
#         # Convert strings to datetime objects
#         start_date = datetime.strptime(start_date, '%Y-%m-%d')
#         end_date = datetime.strptime(end_date, '%Y-%m-%d')

#         query = {
#             "name": "Alice",
#             "$or": [
#                 {"symptoms.date": {"$gte": start_date, "$lte": end_date}},
#                 {"past_diagnoses.date": {"$gte": start_date, "$lte": end_date}},
#                 {"allergies.date": {"$gte": start_date, "$lte": end_date}},
#                 {"medications.date": {"$gte": start_date, "$lte": end_date}},
#             ]
#         }

#         # Query the database
#         result = db.find(query)
#         return list(result)  # Return the results as a list

#     except Exception as e:
#         return {"error": str(e)}

@tool("query-db-tool", args_schema=QueryDB, return_direct=True)
def query_db(name: str, fields: Optional[List[str]] = None, dates: Optional[Tuple[str, str]] = None) -> Any:
    """Query the database for a user by name, and optionally filter by a combination of fields and date range"""
    
    start_date, end_date = None, None
    if dates:
        start_date, end_date = dates
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # Fetch the user document based on the unique name
    user_data = db.find_one({"name": "Alice"})
    if not user_data:
        return {"error": "User not found"}

    # If no specific fields are provided, fetch all fields
    fields_to_fetch = fields or {"allergies", "medications", "symptoms", "past_diagnoses", "health_conditions"}

    # Filter the data based on the provided fields
    filtered_data = {}
    for field in fields_to_fetch:
        if field in user_data:
            # Filter entries by date range if start_date and end_date are provided
            if start_date and end_date:
                filtered_data[field] = [
                    item for item in user_data[field]
                    if start_date <= item['date'] <= end_date
                ]
            else:
                filtered_data[field] = user_data[field]

    return filtered_data
    
    
    
