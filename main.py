import os 
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from google import genai

app = FastAPI(title="AI Tóm Tắt Văn Bản Của Tôi Sử Dụng Gemini")
class Item(BaseModel) :
    text : str

@app.post("/tom-tat")
def process_text (item : Item) :
    input_text =  item.text
    words = input_text.split()
    total_word = len(words)
    sentences = input_text.split(".")
    summary = ".".join(sentences[:2])+ "... " if len(sentences) > 2 else input_text
    return {
        "status" :"Success",
        "Total words" : total_word,
        "Tom tat : " : summary
    }

app = FastAPI(title="TRỢ LÝ AI")
# 1. Bật cấu hình cho phép các thiết bị có thể kết nối vào ( laptop, pc, mobile)
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_headers=["*"],allow_methods=["*"],)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key= GEMINI_API_KEY) if GEMINI_API_KEY else None
class ChatRequest(BaseModel) :
    prompt : str 

@app.get("/")
def home(): 
    return {"message" : "Server Backend still works normally"}
@app.post("/chat")
def chat_with_ai(request : ChatRequest) :
    
    model_to_try = ["gemini-1.5-flash","gemini-1.5-flash-8b",    # Bản siêu nhẹ, rất hiếm khi hết quota
    "gemini-2.0-flash-lite", # Bản lite của 2.0
    "gemini-2.0-flash"]
    last_error =""
    for model_name in model_to_try:
        try : 
                response = client.models.generate_content(model=model_name,contents=request.prompt)
                if response.text : 
                    return {
                        "status " :"SUCCESS",
                        "YOUR QUESTION " : request.prompt,
                        "AI's ANSWER" : response.text
                    }
        except Exception as e :
            last_error = str(e)
            continue
    return {
        "status" : "ERROR",
        "ERROR DETAILS" : last_error
    }
            
