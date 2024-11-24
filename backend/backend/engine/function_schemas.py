from pydantic import BaseModel, Field

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

class QueryDateRange(BaseModel):
    name: str = Field(
        description="Name of the user."
    )
    start_date: str = Field(
        description="start date in 'YYYY-MM-DD' format"
    )
    end_date: str = Field(
        description="end date in 'YYYY-MM-DD' format"
    )

class QueryField(BaseModel):
    name: str = Field(
        description="Name of the user."
    )
    field: str = Field(
        description="Field to query information, select out of allergies, medications, symptoms, past_diagnoses"
    )
    

class ReminderSchema(BaseModel):
    description: str = Field(
        description="Why the reminder is being created"
    )
    # reminder_times: list = Field(
    #     description="When should the reminder be triggered"
    # )
    # frequency:int = Field(
    #     description="How frequently should the reminder be repeated"
    # )

