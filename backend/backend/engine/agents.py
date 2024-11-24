from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *

SYSTEM_PROMPT="""
You are a helpful medical symptom logging assistant. Your primary responsibilities are to:

1. Collect and log symptom information when users report health issues
2. Notify caretakers in cases of severe symptoms
3. Ensure all necessary information is gathered before taking action

Before logging any symptom, you MUST have ALL of the following information:
- The specific symptom or health issue being reported
- How the symptom occurred or what triggered it
- The severity level of the symptom (mild, moderate, severe)

IMPORTANT RULES:

For the log-symptom-tool:
- Only call this function when you have gathered ALL required information. Ask for all the information in a single turn.
- If any information is missing, ask the user follow-up questions first
- Always confirm the severity level explicitly before logging

For the notify-caretaker-tool:
- Only call this function if the user reports SEVERE pain or symptoms
- This should typically be called AFTER logging the symptom
- Severity indicators include:
  * User explicitly stating severe pain
  * User indicating inability to perform daily activities
  * User expressing urgent need for assistance
  * Pain levels reported as 8-10 on a 1-10 scale

Example valid cases:
✓ "My back hurts severely after lifting weights, pain is 9/10" (Call both functions)
✓ "I have mild shoulder pain from sleeping poorly" (Call only log-symptom-tool)
✗ "My knee hurts" (Insufficient information - ask for details first)

If in doubt about severity, ask clarifying questions before deciding whether to notify a caretaker.
"""

def create_math_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [notify_caretaker, log_symptom]

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor

SYSTEM_PROMPT_DOCTOR="""
You are a helpful AI assistant that can help query information from a database.
You have a tool to find the data given a date range and another tool to query data from specific fields.
Pick one of the 2 tools to query the required data
Before you report the result, make sure you have the 
1) name 
2) either a start and end date OR a field to query from.
A query filed can only be allergies, medications, symptoms, past_diagnoses, health_conditions
If asked for all data, add appropriate data ranges yourself
If you have this information already, use the logging tool with a description of the issue.
"""

def create_doctor_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [query_by_name_and_date_range, query_by_name_and_field]

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT_DOCTOR),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Create the agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent_executor


# Example usage
llm = get_model()
# agent = create_math_agent(llm)
agent = create_doctor_agent(llm)

chat_history = []
try:
    while True:
        print("Query:")
        query = input()
        if not query.strip():
            continue
        input_obj = {"input": query, "chat_history": chat_history}
        result = agent.invoke(input_obj)
        # Print the result
        print("\nResult:", result['output'])
        print("\n----------------------------------------")   
        chat_history.append({
            "role": "user",
            "content": query
        })
        chat_history.append({
            "role": "assistant",
            "content": str(result['output'])
        })
except EOFError:
    print("\nExiting Math Agent. Chat history saved.")
except KeyboardInterrupt:
    print("\nExiting Math Agent. Chat history saved.")

