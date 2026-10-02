import os
import json
from dotenv import load_dotenv
load_dotenv()

from tavily import TavilyClient 
from google import genai
from google.genai import types
memory_file = "longterm.json"
# 1. Initialize the client (uses GEMINI_API_KEY environment variable)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# 2. Define a tool function with type hints and docstring
