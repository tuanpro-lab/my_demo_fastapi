''' save files for one session'''
import os 
import json
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI(api_key=os.getenv("AGENTIC_API_KEY"))
client_1 = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
class SessionChat :
    def __init__(self,session_id : str, storage_dir : str = "./sessions"):
        self.session_id = session_id
        self.file_path = os.path.join(storage_dir,f"{session_id}.json")
        os.makedirs(storage_dir,exist_ok= True) 
        self.history = self._loadHistory()
        self.currentchat = [] 
    def _loadHistory(self,previous_session = 1) -> list  :
        if os.path.exists(self.file_path) :
            with open(self.file_path,"r",encoding="utf-8") as f : 
                summaries = json.load(f) 
            recent =  summaries[:previous_session]
            res = []
            for s in recent : 
                res.append()

        return []
    def startSession(self) :  
        requests = input(str())
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=requests,
            config=types.GenerateContentConfig(
                tools=[],
            ),
        )
        self.currentchat.append((f"{requests}",f"{response.text}"))
    def summary_chat(self) : 
        ''' compact all chat session in 200-300 meaning words that can be easily to store and retrieve.
        What techniques often use to this ?  
        - save to this {session_id}.json
        ''' 
        conversation_text = ""
        for msg in self.currentchat :  
            content = msg[1]
            conversation_text += f"{content}\n\n"
        prompt=f"""Summarize conversation_text into a structured Json format with these fiels : 
        - main_topics : What are the main topics that I want to dicuss(list of strings)
        - User's facts : the important things that user shares about themselves(list of strings) -> change to procedural memory 
        - Conclusions : decisions or conclusions reached(list of strings)
        - Pending tasks : unfinished tasks or follow-ups needed(list of strings)
        return only valid Json, no explanation
        Conversation : {conversation_text}
        """
        response = client_1.chat.completions.create(
            model="DeepSeek-R1",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        result = response.choices[0].message.content.strip()
        try : 
            structured = {"summary" : result}
        except json.JSONDecodeError as e : 
            return e.msg
        session_data = {
            "session_id" : self.session_id
            **structured
        }
        return session_data
    def _saveHistory(self) :
        summaries = []
        if os.path.exists(self.file_path) :
            with open(self.file_path,"r",encoding= "utf-8") as f :
                summary = json.load(f)
        summaries.append(summary)
        with open(self.file_path,"w",encoding = "utf-8") as f : 
            json.dump(summaries,f,ensure_ascii=True,indent=2)

        
    

         
    
    