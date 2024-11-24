# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from datetime import datetime

# # MongoDB URI
# uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# # Select the database and collection
# db = client['client_db']
# collection = db['users']

# # Define the valid_user object
# valid_user = {
#     "name": "Alice",  # Name is required and must be a string
#     "age": 30,  # Age is required and must be an integer >= 18
#     "email": "alice@example.com",  # Email is required and must be a string
#     "gender": "female",  # Gender is optional but must be a string if present
#     "weight": 65.5,  # Weight is optional but must be a double (float)
#     "height": 167.2,  # Height is optional but must be a double (float)
#     "medications": [
#         {"name": "chloramphenicol", "date": datetime(2023, 6, 1), "description": "treating meningitis"},
#         {"name": "penicillin", "date": datetime(2023, 7, 1), "description": "no specific details given"}
#     ]
# }

# try:
#     # Update the document with the name "Alice"
#     result = collection.update_one(
#         {"name": "Alice"},  # Filter to find the document
#         {"$set": valid_user},  # Update the document with valid_user fields
#         upsert=True  # If no document is found, insert a new one
#     )
#     print(f"Matched {result.matched_count} document(s).")
#     print(f"Modified {result.modified_count} document(s).")
# except Exception as e:
#     print("An error occurred:", e)


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

# MongoDB URI
uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Select the database and collection
db = client['client_db']
collection = db['users']

# New medications to append
new_medications = [
    {"name": "chloramphenicol", "date": datetime(2023, 6, 1), "description": "treating meningitis"},
    {"name": "penicillin", "date": datetime(2023, 7, 1), "description": "no specific details given"}
]

try:
    # Append the new medications to the medications array for the user with name "Alice"
    result = collection.update_one(
        {"name": "Alice"},  # Filter to find the document
        {"$push": {"medications": {"$each": new_medications}}},  # Append new medications
        upsert=False  # Do not insert if the document does not exist
    )
    print(f"Matched {result.matched_count} document(s).")
    print(f"Modified {result.modified_count} document(s).")
except Exception as e:
    print("An error occurred:", e)
