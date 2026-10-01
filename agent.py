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
def recall_memories() : 
    """ Recall some necessary fact in long_term memory """
    memories = load_long_term_memory() 
    if not memories :
        return "No long_term memories found."
    else :
        pass 
    ''' use hierachy memories to decide which one is suitable for each context '''
#3 . Create memory to retrieve when necessary ( distinguish between when use short/longterm) 
def load_long_term_memory() : # problem you don't need to call all the information in longterm --> how optimize that 
    if os.path.exists(memory_file) :
        with open(memory_file,"r",encoding="utf-8") as f :
            return json.load(f)
    return [] 
    '''use semantic and '''
def save_memories() : 
    pass
# 3. Send prompt with tool enabled
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=input(str()),
    config=types.GenerateContentConfig(
        tools=[],
    ),
)

print(response.text)