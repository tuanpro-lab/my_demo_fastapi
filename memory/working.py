''' save files for one session'''
import os 
import json
from google import genai 
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
class SessionMemory :
    def __init__(self,session_id : str, storage_dir : str = "./sessions"):
        self.session_id = session_id
        self.file_path = os.path.join(storage_dir,f"{session_id}.json")
        os.makedirs(storage_dir,exist_ok= True) 
        self.history = self._loadHistory() 
    def _loadHistory(self) -> list  :
        if os.path.exists(self.file_path) :
            with open(self.file_path,"r",encoding="utf-8") as f : 
                return json.load(f) 
        return []
    def _saveHistory(self) :
        with open(self.file_path,"w",encoding = "utf-8") as f : 
            json.dump(self.history,f,ensure_ascii=True,indent=2)
    def startSession(self) :  
        requests = input(str())
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=requests,
            config=types.GenerateContentConfig(
                tools=[],
            ),
        )
        self.history.append(f"User : {requests} . AI's response : {response.text}")
    def CompactSession(self) : 
        pass 

        
    

         
    
    