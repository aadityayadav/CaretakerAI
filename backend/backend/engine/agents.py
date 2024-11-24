from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *

SYSTEM_PROMPT="""
You are a helpful AI assistant that can help elderly people report their issues or create reminders.
You have a tool that logs symptoms if the user mentions any issues they face and a tool to create reminders
Before you report a symptom, make sure you have:
- What the issue is
- When it started
- The severity of the symptom
Before you create a reminder make sure you have:
- What the reminder is for
If you have this information already, use the logging tool with a description of the issue.
"""

def create_math_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [log_symptom, reminder]

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
agent = create_math_agent(llm)

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

