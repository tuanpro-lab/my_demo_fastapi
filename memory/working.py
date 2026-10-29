''' save files for one session'''
import episodic
from datetime import datetime,timezone
import atexit
import os 
import requests 
import json
import uuid
# use files for storing all conversation chats with AI and db for storing the most important info
# store short amount of context updating immediately 
url = "http://localhost:11434/api/generate"
think_model ="deepseek-r1:1.5b"
chat_model = "qwen2.5vl:3b"
class SessionChat :
    def __init__(self,session_id = str(uuid.uuid4()) , storage_dir : str = "./sessions"):
        self.session_id = session_id
        self.file_path = os.path.join(storage_dir,f"{self.session_id}.json")
        os.makedirs(storage_dir,exist_ok= True) 
        self.context = self._load_previousChat()
        self.currentchat = [] 
    def _load_previousChat(self) -> str  :
        try : 
            recent = episodic.EpisodicMemory().get_important_feature(self.session_id)
            current_context = ""
            for s in recent : 
                current_context += f"main topics: {', '.join(s.get('main_topics', []))}." + " "
                current_context += f"pending tasks: {', '.join(s.get('pending_tasks', []))}." 
            return current_context 
        except Exception :
            print("SESSION DOESN'T HAVE PREVIOUS CHAT")
            return ""
    def summary_chat(self) : 
        ''' compact all chat session in 200-300 meaning words that can be easily to store and retrieve.
        What techniques often use to this ?  
        - save to this {session_id}.json
        ''' 
        conversation_text = ""
        for msg in self.currentchat :  
            content = msg[1]
            conversation_text += f"{content}\n\n"
        prompt=f"""You are a helpful AI assistant.Summarize conversation_text into a structured Json format with these fiels : 
        - main_topics : What are the main topics that I want to dicuss(list of strings)
        - user's facts : the important things that user shares about themselves(list of strings).If user don't provide anything . return [] 
        - conclusions : decisions or conclusions reached(list of strings)
        - pending tasks : unfinished tasks or follow-ups needed(list of strings)
        return only valid Json, no explanation
        Conversation : {conversation_text}
        """
        res = requests.post(url,json = {
            "model" : chat_model,
            "prompt" :  prompt,
            "stream" : False ,
            "format" : json,
        })
        try : 

            structured = {res}
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
    def startSession(self) :  
        """the problem here is that i don't know when to use context,retrieve in order to increase
        the efficiency of input and give LLM more context to get better ans
        """
        while True :
            prompt = input(str())
            current_time = datetime.now(timezone.utc).isoformat()
            """ each conversation store filepath"""
            response = requests.post(url,json = {
                "model" : chat_model,
                "prompt" : prompt,
                "stream" : True,
            })
            with open(self.file_path,"w",encoding="utf-8") as f : 
                one_chat = [current_time,prompt,response]
                f.write("\n".join(one_chat))
    def manage_context(self) : 
        pass 


if __name__=="__main__" : 
    session = SessionChat()
    atexit.register(session.summary_chat()) 
    atexit.register(session._saveHistory())
    s = session.startSession()



       

        
    

         
    
    