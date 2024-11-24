from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# client = MongoClient(uri, tlsCAFile=certifi.where())

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Connect to the database
    db = client["client_db"]

    # Define updated validation rules for the "users" collection
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
                }
            }
        }
    }

    # Create the "users" collection with validation
    db.create_collection("users", validator=validation)

    print("Collection created with schema validation.")

    print("Collection created with updated schema validation.")

    from datetime import datetime

    valid_user = {
        "name": "Alice",  # Name is required and must be a string
        "age": 30,  # Age is required and must be an integer >= 18
        "email": "alice@example.com",  # Email is required and must be a string
        "gender": "female",  # Gender is optional but must be a string if present
        "weight": 65.5,  # Weight is optional but must be a double (float)
        "height": 167.2,  # Height is optional but must be a double (float)
        "symptoms": [
            {"description": "fever", "date": datetime(2023, 11, 1)},  # Symptoms must be an array of objects with a description and date
            {"description": "headache", "date": datetime(2023, 11, 2)}
        ],
        "past_diagnoses": [
            {"name": "hypertension", "description": "High blood pressure", "doctor_name": "Dr. Smith", "date": datetime(2022, 1, 15)},
            {"name": "diabetes", "description": "Type 2 diabetes", "doctor_name": "Dr. Johnson", "date": datetime(2021, 7, 10)}
        ],
        "allergies": [
            {"name": "penicillin", "date": datetime(2020, 3, 5)},
            {"name": "pollen", "date": datetime(2022, 6, 15)}
        ],
        "medications": [
            {"name": "losartan", "date": datetime(2023, 6, 1), "description": "For blood pressure", "dosage": "50mg", "frequency": "once daily"},
            {"name": "metformin", "date": datetime(2023, 6, 1), "description": "For diabetes", "dosage": "500mg", "frequency": "twice daily after meals"}
        ]
    }

    # Insert the valid user into the "users" collection
    db.users.insert_one(valid_user)
    print("Valid user inserted successfully.")

except Exception as e:
    print(e)

