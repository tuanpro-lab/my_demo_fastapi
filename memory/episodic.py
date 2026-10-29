''' often need vector databases'''
import sqlite3
import uuid
from dataclasses import dataclass,field
import numpy as np
from datetime import datetime,timezone
from typing import Sequence
from sentence_transformers import SentenceTransformer
# define connection and cursor 
class EpisodicMemory : 
    def __init__(self,path_db = "memory.db",sematic_weight = 0.7,):
        #weights = [semantic_weight,lexical_weight,importance_weight,recency_weight]
        self.connect = sqlite3.connect(path_db)
        self._refresh_session_ids()


    def initialize_db(self) : 
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
    def _refresh_session_ids(self) : 
        rows = self.cursor.execute("SELECT session_id FROM episodes").fetchall() 
        self.id_exist = {session_id for (session_id,) in rows}
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
            self.connect.commit()
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
            self.connect.commit()
    def get_important_feature(self,session_id) : 
        # use this for get the most important infomation providing for 
        if session_id not in self.id_exist :
            raise ValueError("SESSION_ID NOT EXIST")
        else : 
            history = self.cursor.execute(
                """ 
                    SELECT * FROM sessionchat
                    WHERE session_id = ? 
                """, (session_id),
            ).fetchall()
            return [{
                "user_fact" : history[3],
                "main_topic" : history[4],
                "conclusions" : history[5],
                "pending_tasks" : history[6],
            }]
    def retrieve(self,query,session_id,limit : int = 5,) :
        pass 

class SentenceTransformerEmbedder : 
    """Local embeddings using Sentence Transformers."""

    def __init__(self,base_model ="paraphrase-multilingual-MiniLM-L12-v2" ):
        self.model_name = base_model
        self.top_k = 5
        self.model = SentenceTransformer(base_model)
    def encode(self,text:Sequence[str]) -> np.ndarray :
        vectors = self.model.encode(list(text),convert_to_numpy = True,normalize_embeddings = True,
                                show_progress_bar = False,) 
        return np.asarray(vectors,dtype=np.float32)
    def semantic_search_manual(self,mostK_relevant,querys : list[str]) : 
        for query in querys :
            query_embedder = self.encode(query)
            
            similarity_score = self.model.similarity(query_embedder,)
''' define the evaluation metrics '''
@dataclass
class RetrieveEpisode : 
    episodes : dict 
    score: float 
    semantic_score: float 
    lexical_score : float 
    recency_score : float 
''' each criterias stand for : ... '''

""" calculate cosine similarity between two vectors"""
def cosine_smilarity(vec1, vec2) :
    dot_product = np.dot(vec1,vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    if norm_vec1 == 0 or norm_vec2 == 0 : return 0.0
    return  dot_product / (norm_vec1 * norm_vec2)

        
        