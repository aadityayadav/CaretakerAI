from backend.engine.function_schemas import *
from langchain.tools import tool
from typing import Any
import json

@tool("calculate-tool", args_schema=CalculateInputsSchema, return_direct=True)
def calculate(expression: str) -> Any:
    """Evaluate a mathematical expression""" 
    try:
        result = eval(expression)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps({"error": f"Invalid expression: {str(e)}"})
