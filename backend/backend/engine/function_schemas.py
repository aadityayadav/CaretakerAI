from pydantic import BaseModel, Field
from typing import Optional, List, Tuple

class CalculateInputsSchema(BaseModel):
    expression: str = Field(
    description="The mathematical expression to evaluate",
    examples=["2 + 2", "5 * 10", "100 / 4"],
    min_length=1,
    max_length=100
    )

class LogSymptomSchema(BaseModel):
    description: str = Field(
        description="Description of the symptom faced by user.",
    )


# class QueryDateRange(BaseModel):
#     name: str = Field(
#         description="Name of the user."
#     )
#     start_date: str = Field(
#         description="start date in 'YYYY-MM-DD' format"
#     )
#     end_date: str = Field(
#         description="end date in 'YYYY-MM-DD' format"
#     )

class QueryDB(BaseModel):
    name: str = Field(
        description="Name of the user to be searched for."
    )
    fields: Optional[List[str]] = Field(
        description="Field(s) to extract information from.",
        allowed_values="allergies,medications,symptoms,past_diagnoses,health_conditions",
        default=None
    )
    dates: Optional[Tuple[str, str]] = Field(
        description="Tuple of the start and end dates to filter from in YYYY-MM-DD format",
        examples="(2024-01-01, 2024-12-31)",
        default=None
    )
    
class ReminderSchema(BaseModel):
    description: str = Field(
        description="The topic of reminder."
    )

class SendEmailSchema(BaseModel):
    contents: str = Field(
        description= "The user's description of the issue as reported by the user themself"

    )
