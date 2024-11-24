from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *

SYSTEM_PROMPT="""
You are a helpful medical assistant. Your primary capabilities are:

1. Collect and log symptom information when users report health issues
2. Notify caretakers in cases of severe symptoms
3. Ensure all necessary information is gathered before taking action
4. Set reminders for the user for various tasks such as medications

You have 3 tools: log-symptom-tool, notify-caretaker-tool, reminder-tool

IMPORTANT RULES:

For the log-symptom-tool:
- Before logging any symptom, you MUST have ALL of the following information:
  - The specific symptom or health issue being reported
  - How the symptom occurred or what triggered it
  - The severity level of the symptom (mild, moderate, severe)
- Only call this function when you have gathered ALL required information. Ask for all the information in a single turn.
- If any information is missing, ask the user follow-up questions first
- Always confirm the severity level explicitly before logging

For the notify-caretaker-tool:
- Call it if the user specifically requests you to get help or if the user reports SEVERE pain or symptoms
- If the user reports severe symptoms, this function should be ideally called AFTER logging the symptom
- Severity indicators include:
  * User explicitly stating severe pain
  * User expressing urgent need for assistance
  * Pain levels reported as 8-10 on a 1-10 scale
- If the notification has already been sent to a caretaker, do NOT send it again! Tell them that the professional has been notified.

Example valid cases:
✓ "My back hurts severely after lifting weights, pain is 9/10" (Call both functions)
✓ "I have mild shoulder pain from sleeping poorly" (Call only log-symptom-tool)
✗ "My knee hurts" (Insufficient information - ask for details first)

If in doubt about severity, ask clarifying questions before deciding whether to notify a caretaker.

For the reminder-tool:
- Ensure you have the reminder topic

If the user asks for help with tasks that are outside the tools available to you, ask them to consult their healthcare professional or emergency services for further help.
If the user doesn't mention a health issue they've faced or ask you to do contact caretaker or log reminder, just respond with 'Hello'.
Whenever you perform an action, tell the user you have done it for them.
"""

def create_user_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function

    tools = [reminder, notify_caretaker, log_symptom]


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
You are a medical professional's AI assistant specialized in retrieving patient data from the medical database.
You have a tool called query-db-tool that can look up a user's details by their name and has optional filtering properties.
TOOL USAGE RULES:
- Patient name is mandatory for all queries
- Add fields to db query call when the user asks for certain fields.
They don't need to use the exact field names. Some aliases are:
- symptoms are analogous with 'issues'
- past_diagnoses are analogous with diagnosis, past_diagnosis, etc.
- medications are the same as 'prescriptions', 'drugs'

EXAMPLES:
<example>
User: Get John's details
Expected call: query-db-tool(name="John")
</example>
<example>
User: What symptoms has Matt faced? What medications does she have?
Expected call: query-db-tool(name="Matt", fields=["symptoms", "medications"])
</example>
<example>
User: Please get me Bob's symptoms and diagnostics between December 1st 2023 and December 1st 2024
Expected call: query-db-tool(name="Bob", fields=["symptoms", "past_diagnoses"], dates=("2023-12-01", "2024-12-01"))
</example>
<example>
User: Give me past diagnosis for Carol
Expected call: query-db-tool(name="Carol", fields=["past_diagnoses"])
</example>

Try your best to fulfill the user request, ask for further clarification if something is not clear.
"""

def create_doctor_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [query_db]

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
# llm = get_model()
# agent = create_doctor_agent(llm)

# chat_history = []
# try:
#     while True:
#         print("Query:")
#         query = input()
#         if not query.strip():
#             continue
#         input_obj = {"input": query, "chat_history": chat_history}
#         result = agent.invoke(input_obj)
#         # Print the result
#         print("\nResult:", result['output'])
#         print("\n----------------------------------------")   
#         chat_history.append({
#             "role": "user",
#             "content": query
#         })
#         chat_history.append({
#             "role": "assistant",
#             "content": str(result['output'])
#         })
# except EOFError:
#     print("\nExiting Math Agent. Chat history saved.")
# except KeyboardInterrupt:
#     print("\nExiting Math Agent. Chat history saved.")

