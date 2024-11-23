from pydantic import BaseModel, Field

class CalculateInputsSchema(BaseModel):
    expression: str = Field(
    description="The mathematical expression to evaluate",
    examples=["2 + 2", "5 * 10", "100 / 4"],
    min_length=1,
    max_length=100
    )