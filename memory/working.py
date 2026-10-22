''' save files for one session'''
import os 
import json
import uuid
from dotenv import load_dotenv
from openai import OpenAI
client = OpenAI(api_key=os.getenv("AGENTIC_API_KEY"))
client_1 = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
# use files for storing all conversation chats with AI and db for storing the most important info
class SessionChat :
    def __init__(self,session_id = str(uuid.uuid4()) , storage_dir : str = "./sessions"):
        self.session_id = session_id
        self.file_path = os.path.join(storage_dir,f"{self.session_id}.json")
        os.makedirs(storage_dir,exist_ok= True) 
        self.context = self._loadHistory()
        self.currentchat = [] 
    def _loadHistory(self,previous_session = 1) -> str  :
        if os.path.exists(self.file_path) :
            with open(self.file_path,"r",encoding="utf-8") as f : 
                summaries = json.load(f) 
            recent =  summaries[:previous_session]
            current_context = ""
            for s in recent : 
                current_context += f"main topics: {', '.join(s.get('main_topics', []))}." + " "
                current_context += f"pending tasks: {', '.join(s.get('pending_tasks', []))}." 
            return current_context 
        return ""
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
        - user's facts : the important things that user shares about themselves(list of strings).If user don't provide anything . return [] 
        - conclusions : decisions or conclusions reached(list of strings)
        - pending tasks : unfinished tasks or follow-ups needed(list of strings)
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
            summaries.append(self.summary_chat())
            with open(self.file_path,"w",encoding = "utf-8") as f : 
                json.dump(summaries,f,ensure_ascii=True,indent=2)

        
    

         
    
    