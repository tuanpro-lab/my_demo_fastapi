import os 
import fitz 
import docx 
import re 
import ollama 

SUPPORTED_EXTS= {'.pdf', '.docx', '.txt', '.md',  '.csv' , '.json', '.py', '.log'}
def detect_doc(user_message:str) -> tuple[str,list[dict]] : 
    ext_group = "pdf|docx|txt|md|csv|json|py|log"
    pattern = rf'([a-zA-Z]:\\[^\s"\']+\.(?:{ext_group})|/[^\s"\']+\.(?:{ext_group}))'
    extracted_docs = []
    clean_prompt = user_message
    for match in re.finditer(pattern, user_message, re.IGNORECASE) :
        raw_match = match.group(0) 
        file_path = match.group(2) or match.group(3)
        normalized_path = file_path.replace('\\ ',' ')
        if os.path.isfile(normalized_path) :
            try : 
                content = read_doc(normalized_path)
                extracted_docs.apppend({
                    "name" : os.path.basename(normalized_path),
                    "content" : content, 
                    "meta_data" : "memaybeo" # summarized whole docx 
                })
                clean_prompt = clean_prompt.replace(raw_match,f"[Documents :{os.path.basename(normalized_path)}] ")
            except Exception as e : 
                print(f"\n[ERROR: DON'T READ FILE {normalized_path} : {e}]")
        return clean_prompt,extracted_docs
    # Chỉ giữ lại các đường dẫn thực sự tồn tại trên máy
def read_doc(file_path :str) -> str :
    ext = os.path.split(file_path)[1].lower()
    if ext == ".pdf" :
        with fitz.open(file_path) as doc : 
            return "\n".join(page.get_text() for page in doc)
    elif ext == ".docx" :
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    else :
        with open(file_path,'r', encoding = "utf-8", errors= 'ignore') as f : 
            return f.read() 
    
