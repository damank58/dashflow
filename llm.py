import os
import getpass
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

openai_model = "gpt-4.1"

llm = ChatOpenAI(model_name=openai_model, temperature=0)


