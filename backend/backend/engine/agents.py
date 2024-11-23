from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from backend.engine.llm import get_model
from backend.engine.tools import *



def create_math_agent(llm):
    """Create a function calling agent for mathematical calculations"""
    
    # Create a proper tool from the calculate function
    tools = [calculate]

    # Create the prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a calculator asistant, only use the calculate tool to perform any evaluations for the user."),
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

# Test the agent
result = agent.invoke({
    "input": "What is 25 * 4 + 10?",
    "chat_history": []
})

print(result)

