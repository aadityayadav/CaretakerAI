from backend.engine.llm import get_model, get_bio_model
from backend.config.database import MongoDB
from datetime import datetime

db = MongoDB.connect_to_mongodb().users

name = "Alice"

# MongoDB aggregation pipeline
pipeline = [
    {"$match": {"name": name}},  # Match the user by name
    {"$project": {
        "name": 1,  # Include name
        "weight": 1,  # Include weight
        "height": 1,  # Include height
        "age": 1,
        "gender": 1,
        # Include the latest 5 entries for each array field
        "symptoms": {"$slice": ["$symptoms", -5]},
        "past_diagnoses": {"$slice": ["$past_diagnoses", -5]},
        "allergies": {"$slice": ["$allergies", -5]},
        "medications": {"$slice": ["$medications", -5]},
        "health_conditions": {"$slice": ["$health_conditions", -5]}
    }}
]

# Execute the aggregation
result = list(db.aggregate(pipeline))
print(result)

prompt=f"""
You will be provided a user's recent health history in JSON format. 
For each listed property such as 'symptoms', 'health_conditions', 'medications', check for any possible factual inconsistencies in the data. 
Here are examples of some scenarios you should report on if they are detected:
- When the user has two opposite symptom descriptions
- The user was prescribed medication that they are allergic to, or are not recommended given their medical conditions
- There are conflicting set of diagnostics for the user
Only list a discrepancy if you are confident that it may be a potential issue.
For each discrepancy, create a bullet point briefly explaining the issue and the property or properties it affects
Only list the bullet point themselves and nothing else.
<user_information>
{result}
</user_information>
"""

llm = get_model()
response = llm.invoke(["input", prompt])
print(response.content)
