'''  
 problems : when you and AI are talking in real time, you often feed too much info into models that 
can affect the performance of models. How to solve it ? 
'''
import sqlite3
from scipy.spatial.distance import cosine
import re 
import numpy as np 
from typing import Sequence,Any
from sentence_transformers import SentenceTransformer
from sentence_transformers import CrossEncoder
from sentence_transformers import SparseEncoder
"""integrate embedder, retrieve, rerrank all at once"""
class SemanticSearch : 
    def __init__(self,db_path = "memory.db",embedding_model ="paraphrase-multilingual-MiniLM-L12-v2",
                reranker_model:str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.embedding_model = embedding_model
        self.rerank_model = reranker_model 
        self.connection = sqlite3.connect(db_path)
    def retrieve(self,query:str,text:list[str],top_k =5,) :
        pass 

class SemanticChunking : 
    def __init__(self,NUM_CTX, Max_Direct_Char,BreakPoint_Percentile: int = 0.9, Min_Chunk_Chars , Max_Chunk_Chars,Buffer_Size) : 
        self.chat_model = "qwen2.5vl:3b"
        self.embed_model = SemanticSearch().embedding_model
        self.Max_Chunk_Chars = Max_Chunk_Chars 
        self.Num_CTX = NUM_CTX 
        self.Max_Direct_Char = Max_Direct_Char
        self.BreakPoint_Percentile = BreakPoint_Percentile 
        self.Min_Chunk_Chars = Min_Chunk_Chars 
        self.Buffer_Size = Buffer_Size 
    """ *** Function divide the whole text into each sentences ***"""
    def split_sentences(self,text) -> list[str] : 
        # chia thành từng câu   
        raw_sentences = re.split(r'(?<=[.!?…])\s+|\n+', text)
        self.sentences = []
        self.embed_sentences = [] 
        for s in raw_sentences:
            s = s.strip()
            if not s:
                continue
            # Dự phòng nếu gặp dòng dữ liệu quá dài không có dấu ngắt câu
            if len(s) > self.Max_Chunk_Chars:
                for i in range(0, len(s), self.Max_Chunk_Chars):
                    self.sentences.append(s[i : i + self.Max_Chunk_Chars])
                    self.embed_sentences.append(self.encode(self.sentences[-1]))
            else:
                self.sentences.append(s)
                self.embed_sentences.append(self.encode(self.sentences[-1]))
        return self.sentences,self.embed_sentences
    """*** FUNCTION ENCODE EACH SENTENCES INTO VECTOR *** """
    def encode(self,text:Sequence[str]) -> np.ndarray :
        vectors = self.embed_model.encode(list(text),convert_to_numpy = True,normalize_embeddings = True,
                                show_progress_bar = False,) 
        return np.asarray(vectors,dtype=np.float32)
    ''' FUNCTION CALCULATE ALL COSINE SIMILARITY BERTWEEN THE CURRENT AND PREV VECTOR'''
    def build_chunk_cosine_distance(self) -> np.ndarray : 
        len_embeddings = len(self.embed_sentences-1)
        c_dists = np.empty(len_embeddings-1)
        for i in range(1, len_embeddings) : 
            c_dists[i-1] =  cosine(self.embed_sentences[i],self.embed_sentences[i-1])
        return c_dists
    '''FUNCTION SETS THE RULE WHEN BREAKPOINT OCCURS TO SEPERATE TWO PARAGRAPHS IN DOCS WHEN EXCEED THRESHOLD'''
    def generate_breakpoint(self,embeddindgs : list[np.ndarray],start : int =0 , end : int  = None,) -> np.ndarray : 
        """Args : 
                embeddings : List of embedding vectors
                start : starting index of processing, default to 0 
                end : ending index of processing, default to None 
                self.BreakPoint_Percentile : determine significant changes. Default to 0,9
            Output : 
                np.ndarray : indices where breakpoints occur
        """
        if end is not None : 
            embedding_windowed = embeddindgs[start:end] 
        else :
            embedding_windowed = embeddindgs[start:]
        len_embeddings = len(embedding_windowed)
        c_dists = np.empty(len_embeddings-1)
        for i in range(1,len_embeddings) : 
            c_dists[i-1] = cosine(embedding_windowed[i],embedding_windowed[i-1])
        difference_threshold = np.percentile(c_dists,100* self.BreakPoint_Percentile,axis=0)
        difference_exceeding = np.argwhere(c_dists >= difference_threshold).ravel() 
        return difference_exceeding
    def build_chunk_stacks(self,length_threshold :int = 20000) -> np.ndarray : 
        """
        Args : length_threshold : the amount of text chunked considered a valid. Default to 20000
               self.BREAKPOINT_PERCENTILE : determine significant changes 
        
        OUTPUT : the indices represents the breakpoints of chunks 
        """
        s= [(0,len(self.sentences))]
        all_breakpoints = set() 
        while s :
            id_start,id_end = s.pop() 
            updated_breakpoints = self.generate_breakpoint(self.embed_sentences,id_start,id_end)
            updated_breakpoints += id_start 
            updated_breakpoints = np.concatenate()
    def semantic_chunk(self,text : str) -> list[str] : 
        text = text.strip()
        if not text :
            return [] 
        if len(text) <= self.Max_Direct_Char :
            return [text]
        sentences = self.split_sentences(text)

