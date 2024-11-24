from pymongo.server_api import ServerApi
from langchain_openai import ChatOpenAI
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv('GROQ_BASE_URL')
model = os.getenv('GROQ_MODEL')
api_key = os.getenv('GROQ_API_KEY')


"""
Sample call:

llm = get_model()
res = llm.invoke("Hello, what's your name!")
print(res.content)
"""
def get_model():
    llm = ChatOpenAI(base_url=base_url, api_key=api_key, model=model, temperature = 0)
    return llm


validation = {
        "$jsonSchema": {
            "bsonType": "object",  # The root document must be an object
            "required": ["name", "email"],  # The "name" and "email" fields are required
            "properties": {
                "name": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                "age": {
                    "bsonType": "int",
                    "minimum": 18,
                    "description": "must be an integer greater than or equal to 18"
                },
                "email": {
                    "bsonType": "string",
                    "description": "must be a string and is required"
                },
                # New optional fields
                "gender": {
                    "bsonType": "string",
                    "description": "must be a string (gender)"
                },
                "weight": {
                    "bsonType": "double",  # Weight should be a float/double
                    "description": "must be a double (weight in kg)"
                },
                "height": {
                    "bsonType": "double",  # Height should be a float/double
                    "description": "must be a double (height in cm)"
                },
                # Symptoms, each with a description and a date
                "symptoms": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "description": {
                                "bsonType": "string",
                                "description": "must be a string (symptom description)"
                            },
                            "date": {
                                "bsonType": "date",
                                "description": "must be a date"
                            }
                        },
                        "required": ["description", "date"],  # Both description and date are required
                        "description": "must be an array of objects with a description and date for each symptom"
                    }
                },
                # Past diagnoses with optional description, doctor_name, and date
                "past_diagnoses": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "name": {
                                "bsonType": "string",
                                "description": "must be a string (diagnosis name)"
                            },
                            "description": {
                                "bsonType": "string",
                                "description": "optional description of the diagnosis"
                            },
                            "doctor_name": {
                                "bsonType": "string",
                                "description": "optional name of the doctor who diagnosed"
                            },
                            "date": {
                                "bsonType": "date",
                                "description": "must be a date (diagnosis date)"
                            }
                        },
                        "required": ["name", "date"],  # Name and date are required
                        "description": "must be an array of objects with a name, date, and optional description and doctor_name"
                    }
                },
                # Allergies with name and date
                "allergies": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "name": {
                                "bsonType": "string",
                                "description": "must be a string (allergy name)"
                            },
                            "date": {
                                "bsonType": "date",
                                "description": "must be a date"
                            }
                        },
                        "required": ["name", "date"],  # Both name and date are required
                        "description": "must be an array of objects with a name and date for each allergy"
                    }
                },
                # Medications with name, date, description, dosage, and frequency
                "medications": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "name": {
                                "bsonType": "string",
                                "description": "must be a string (medication name)"
                            },
                            "date": {
                                "bsonType": "date",
                                "description": "must be a date"
                            },
                            "description": {
                                "bsonType": "string",
                                "description": "optional description of the medication"
                            },
                            "dosage": {
                                "bsonType": "string",
                                "description": "optional dosage information"
                            },
                            "frequency": {
                                "bsonType": "string",
                                "description": "optional frequency information (e.g., daily, after meals)"
                            }
                        },
                        "required": ["name", "date"],  # Both name and date are required
                        "description": "must be an array of objects with a name, date, and optional description, dosage, and frequency"
                    }
                },
                "health_conditions": {
                    "bsonType": "array",
                    "items": {
                        "bsonType": "object",
                        "properties": {
                            "name": {
                                "bsonType": "string",
                                "description": "must be a string (condition name)"
                            },
                            "date": {
                                "bsonType": "date",
                                "description": "must be a date"
                            }
                        },
                        "required": ["name", "date"],  # Both name and date are required
                        "description": "must be an array of objects with a name, date"
                    }
                }
            }
        }
    }


# def parse_query(input_text, llm):
#     """Uses the LLM to convert natural language input into a MongoDB query."""
#     prompt = f"""
#     Convert the following natural language query into a MongoDB query using the schema below:

#     Schema: {validation}

#     Query: "{input_text}"

#     MongoDB Query:
#     """
#     response = llm.invoke(["input", prompt])
#     # print(response)
#     query = response.content.strip("'\"`")

#     print(query)
#     # return eval(response["content"])  # Ensure safe evaluation or use a JSON parser
#     # return eval(query)
#     return query


# from pymongo import MongoClient

# def validate_query(query, schema):
#     """Validates the query against the MongoDB validation schema."""


#     uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

#     # Create a new client and connect to the server
#     client = MongoClient(uri, server_api=ServerApi('1'))

#     # Select the database (replace 'your_database' with your database name)
#     db = client['client_db']

#     # Access a collection (replace 'your_collection' with your collection name)
#     collection = db['users']
#     try:
#         collection.insert_one(query)  # Insert to test schema compliance
#         collection.delete_one(query)  # Remove the test entry
#         return True
#     except Exception as e:
#         return False, str(e)

# def execute_query(query):
#     """Executes the validated MongoDB query."""

#     uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

#     # Create a new client and connect to the server
#     client = MongoClient(uri, server_api=ServerApi('1'))
#     db = client["client_db"]
#     collection = db["users"]

#     results = collection.find(query)
#     return list(results)


# def handle_user_query(input_text):
#     llm = get_model()

#     # Step 1: Parse Query
#     query = parse_query(input_text, llm)

#     # Step 2: Validate Query
#     is_valid, error = validate_query(query, validation)
#     if not is_valid:
#         return {"error": f"Validation failed: {error}"}

#     # Step 3: Execute Query
#     results = execute_query(query)

#     # Step 4: Return Results
#     return {"query": query, "results": results}

import json

def parse_query(input_text, llm):
    """Uses the LLM to convert natural language input into a MongoDB query."""
    prompt = f"""
    Convert the following natural language query into a MongoDB query using the schema below:

    Schema: {validation}

    Query: "{input_text}"

    REQUIRED FIELDS, NEEDED WITH EACH CALL:  "name": "Alice", "email": "alice@example.com"

    ONLY RETURN THE QUERY AND NOTHING ELSE 

    MongoDB Query:
    """
    response = llm.invoke(["input", prompt])
    print("RESPONSE CALLED: ")
    print(response)
    
    # Get the response content and clean it
    query = response.content.strip("'\"`")

    try:
        # Try parsing the query as a JSON object (MongoDB query is usually JSON-like)
        query_dict = json.loads(query)
    except json.JSONDecodeError as e:
        return {"error": f"Query parsing failed: {str(e)}"}

    print(query_dict)
    return query_dict

def validate_query(query, schema):
    """Validates the query against the MongoDB validation schema."""
    if not isinstance(query, dict):  # Ensure query is a dictionary
        return False, "Query must be a dictionary."

    uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['client_db']
    collection = db['users']

    try:
        # Test the query by attempting to insert it into the database
        collection.insert_one(query)  # This validates the query schema
        collection.delete_one(query)  # Remove the test entry after validation
        return True, None
    except Exception as e:
        return False, str(e)

def handle_user_query(input_text):
    llm = get_model()

    # Step 1: Parse Query
    query = parse_query(input_text, llm)
    if isinstance(query, dict) and "error" in query:
        return query  # Return the error from parse_query

    # Step 2: Validate Query
    is_valid, error = validate_query(query, validation)
    if not is_valid:
        return {"error": f"Validation failed: {error}"}

    # Step 3: Execute Query
    results = execute_query(query)

    # Step 4: Return Results
    return {"query": query, "results": results}

def execute_query(query):
    """Executes the validated MongoDB query."""
    uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client["client_db"]
    collection = db["users"]

    try:
        results = collection.find(query)
        return list(results)
    except Exception as e:
        return {"error": str(e)}

# input_text = "Return all data from 5th june 2020 to today"
# response = handle_user_query(input_text)
# print(response)
input_text = "Return all data from 5th june 2020 to today"
# input_text = "Return all symptoms"

for attempt in range(1, 6):  # Loop up to 5 times
    try:
        print(f"Attempt {attempt}: Handling user query...")
        response = handle_user_query(input_text)

        if isinstance(response, dict) and "error" not in response:
            print("Query successful!")
            print(response)
            break  # Exit the loop if successful
        else:
            print(f"Query failed: {response.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"Exception occurred on attempt {attempt}: {str(e)}")
        break  # Exit the loop if an exception occurs

print("Exiting loop.")
