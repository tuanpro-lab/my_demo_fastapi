''' often need vector databases'''
import sqlite3
import uuid
from datetime import datetime,timezone
# define connection and cursor 
class EpisodicMemory : 
    def __init__(self,path_db = "memory.db"):
        self.id_exist = set()
        self.connect = sqlite3.connect(path_db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("PRAGMA foreign_keys =ON;")
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id String NOT NULL,
                    created_at String NOT NULL,
                );
            """
        )
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sessionchat (
                    session_id String PRIMARY KEY NOT NULL,
                    created_at Sting NOT NULL,
                    updated_at String ,
                    user_fact TEXT ,
                    main_topic TEXT NOT NULL , 
                    conclusions TEXT, 
                    pending_task TEXT,
                    FOREIGN KEY(session_id) REFERENCES episodes(session_id) ON DELETE CASADE 
                );
            """
        )
    def add(self,session_id,user_fact,main_topic,conclusions,pending_tasks) : 
        if session_id not in self.id_exist : 
            created_at = datetime.now(timezone.utc).isoformat()
            self.id_exist.add(session_id)
            with self.cursor :
                self.cursor.execute(
                    """
                        INSERT INTO episodes (
                            session_id,
                            created_at,
                        )
                        VALUES (?,?)
                    """,(session_id,created_at)
                )
                self.cursor.execute(
                    """
                        INSERT INTO sessionchat (
                            session_id,created_at,
                            user_fact,main_topic,conclusions,pending_tasks
                        )
                        VALUES(?,?,?,?,?,?)
                    """,(session_id,created_at,main_topic,conclusions,pending_tasks)
                )
        else : 
            updated_at = datetime.now(timezone.utc).isoformat()
            self.cursor.execute(
                """
                    INSERT INTO sessionchat (
                        updated_at,user_fact,
                        main_topic,conclusions,pending_tasks
                    )
                    VALUES(?,?,?,?,?,?)
                """,(updated_at,user_fact,main_topic,conclusions,pending_tasks)
            )
    def get(self,session_id) : 
        # use this for 
        if session_id not in self.id_exist :
            raise Exception("SESSION_ID NOT EXIST")
        else : 
            history = self.cursor.execute(
                """ 
                    SELECT * FROM sessionchat
                    WHERE session_id = ? 
                """
            )
            return history
        
        
        