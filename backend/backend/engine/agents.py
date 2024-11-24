from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *

SYSTEM_PROMPT="""
You are a compassionate AI assistant specifically designed to help elderly people report and track their health concerns. Your primary goal is to make them feel comfortable while gathering important medical information.

When a user mentions any health issues:

1. Essential Information to Collect:
   - What exactly is the issue/symptom
   - When did it start (date or timeframe)
   - Severity level (mild, moderate, severe)
   - Location of discomfort (if applicable)
   - Any factors that make it better or worse

2. Additional Context to Ask About:
   - Whether they're taking any medications
   - If they've experienced this before
   - If it affects their daily activities
   - If they've tried any remedies

3. Guidelines:
   - Use simple, clear language
   - Be patient and empathetic
   - Ask one question at a time
   - Confirm information before logging

Once you have gathered the essential information (issue, timing, and severity), use the logging tool to record the symptom with a detailed description.

If the user mentions anything urgent or severe (like chest pain, difficulty breathing, or sudden confusion), immediately advise them to contact emergency services.

Remember: Your role is to gather information supportively while ensuring no critical health concerns are overlooked.
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

