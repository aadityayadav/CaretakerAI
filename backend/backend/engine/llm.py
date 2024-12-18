from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

base_url = os.getenv('GROQ_BASE_URL')
model = os.getenv('GROQ_MODEL')
api_key = os.getenv('GROQ_API_KEY')

base_url_1 = os.getenv('NEBIUS_BASE_URL')
api_key_1 = os.getenv('NEBIUS_API_KEY')
model_1=os.getenv('NEBIUS_MODEL')

"""
Sample call:

llm = get_model()
res = llm.invoke("Hello, what's your name!")
print(res.content)
"""
def get_model():
    llm = ChatOpenAI(base_url=base_url, api_key=api_key, model=model, temperature=0.0)
    return llm

def get_bio_model():
    llm = ChatOpenAI(base_url=base_url_1, api_key=api_key_1, model=model_1, temperature=0.0)
    return llm