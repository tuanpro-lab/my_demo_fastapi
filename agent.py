import os
import json
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6LWYfD9dNCG4clPN65SJui_Y0vLXzboz71JjGBAD63irw"
os.environ["TAVILY_API_KEY"] = "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"
memory_file = "longterm.json"
from tavily import TavilyClient 
from google import genai
from google.genai import types

# 1. Initialize the client (uses GEMINI_API_KEY environment variable)
client = genai.Client()
tavily = TavilyClient()

# 2. Define a tool function with type hints and docstring
def web_search(query : str) -> str:
    ''' Search the web using current information using Tavily'''
    results = tavily.search(query=query, max_results= 2)
    output = []
    for r in results :
        output.append(f"- {r['title']}: {r['content'][:300]}")
    return "\n".join(output)
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