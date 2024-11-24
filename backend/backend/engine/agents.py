from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *

SYSTEM_PROMPT="""
You are a helpful AI assistant that can help elderly people report their issues.
You have a tool that logs symptoms if the user mentions any issues they face.
Before you report a symptom, make sure you have:
- What the issue is
- When it started
- The severity of the symptom
If you have this information already, use the logging tool with a description of the issue.
"""

def create_math_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [calculate, log_symptom]

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

# Example usage
llm = get_model()
agent = create_math_agent(llm)

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

