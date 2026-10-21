''' often need vector databases'''
import sqlite3


# define connection and cursor 
class EpisodicMemory : 
    def __init__(self,path_db = "memory.db"):
        self.connect = sqlite3.connect(path_db)
        self.cursor = self.connect.cursor()
        self.cursor.execute("PRAGMA foreign_keys =ON;")
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS episodes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp Sting NOT NULL,
                    session_id String NOT NULL,
                );
            """
        )
        self.cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS sessionchat (
                    session_id TEXT PRIMARY KEY NOT NULL,
                    created_at Sting NOT NULL,
                    updated_at String NOT NULL,
                );
            """
        )
        
        