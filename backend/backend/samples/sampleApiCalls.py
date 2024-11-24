
from datetime import datetime
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://aadityayadav2003:j8EKQQ7fwpvzm6d5@metacluster.9wjb6.mongodb.net/?retryWrites=true&w=majority&appName=MetaCluster&tlsAllowInvalidCertificates=true"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Select the database (replace 'your_database' with your database name)
db = client['client_db']

# Access a collection (replace 'your_collection' with your collection name)
collection = db['users']

def query_by_name_and_date_range(name, start_date, end_date):
    """
    Query all relevant data for a user with the specified name and a date range
    for symptoms, past diagnoses, allergies, and medications.
    
    :param name: Name of the user
    :param start_date: Start date in 'YYYY-MM-DD' format
    :param end_date: End date in 'YYYY-MM-DD' format
    :return: MongoDB query results
    """
    try:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = {
            "name": name,
            "$or": [
                {"symptoms.date": {"$gte": start_date, "$lte": end_date}},
                {"past_diagnoses.date": {"$gte": start_date, "$lte": end_date}},
                {"allergies.date": {"$gte": start_date, "$lte": end_date}},
                {"medications.date": {"$gte": start_date, "$lte": end_date}}
            ]
        }

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}


def query_by_name_and_field(name, field):
    """
    Query a specific field (e.g., allergies, medications) for a user by name.
    
    :param name: Name of the user
    :param field: Field to query (allergies, medications, etc.)
    :return: MongoDB query results
    """
    try:
        if field not in ["allergies", "medications", "symptoms", "past_diagnoses"]:
            return {"error": "Invalid field specified. Valid fields are: allergies, medications, symptoms, past_diagnoses."}

        query = { "name": name }

        # Add the specified field to the query
        query[field] = {"$exists": True}

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}


def query_by_name_and_symptom(name, symptom_description):
    """
    Query for specific symptoms for a user by name and symptom description.
    
    :param name: Name of the user
    :param symptom_description: The description of the symptom
    :return: MongoDB query results
    """
    try:
        query = {
            "name": name,
            "symptoms.description": symptom_description
        }

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}


def query_by_name_and_medication_date(name, start_date, end_date):
    """
    Query medications for a user by name and within a date range.
    
    :param name: Name of the user
    :param start_date: Start date for the medication date range
    :param end_date: End date for the medication date range
    :return: MongoDB query results
    """
    try:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = {
            "name": name,
            "medications.date": {"$gte": start_date, "$lte": end_date}
        }

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}



def query_by_name_and_past_diagnoses(name, start_date, end_date):
    """
    Query past diagnoses for a user by name and within a date range.
    
    :param name: Name of the user
    :param start_date: Start date for the diagnosis date range
    :param end_date: End date for the diagnosis date range
    :return: MongoDB query results
    """
    try:
        # Convert strings to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        query = {
            "name": name,
            "past_diagnoses.date": {"$gte": start_date, "$lte": end_date}
        }

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}


def query_by_name_and_demographics(name, age=None, gender=None):
    """
    Query a user's demographic data (age, gender) along with their name.
    
    :param name: Name of the user
    :param age: Optional age filter
    :param gender: Optional gender filter
    :return: MongoDB query results
    """
    try:
        query = {"name": name}

        if age:
            query["age"] = age
        if gender:
            query["gender"] = gender

        # Query the database
        result = collection.find(query)
        return list(result)  # Return the results as a list

    except Exception as e:
        return {"error": str(e)}





# Query data for a user named "John Doe" within a date range for symptoms
user_query = query_by_name_and_date_range("John Doe", "2023-01-01", "2023-12-31")
print(user_query)

# Query allergies for "John Doe"
allergies_query = query_by_name_and_field("John Doe", "allergies")
print(allergies_query)

# Query a specific symptom for "John Doe"
symptom_query = query_by_name_and_symptom("John Doe", "headache")
print(symptom_query)

# Query medications for "John Doe" within a date range
medication_query = query_by_name_and_medication_date("John Doe", "2023-01-01", "2023-12-31")
print(medication_query)

# Query past diagnoses for "John Doe" within a date range
diagnosis_query = query_by_name_and_past_diagnoses("John Doe", "2023-01-01", "2023-12-31")
print(diagnosis_query)

# Query demographic information for "John Doe"
demographics_query = query_by_name_and_demographics("John Doe", age=30)
print(demographics_query)
