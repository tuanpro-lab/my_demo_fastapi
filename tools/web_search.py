from tavily import TavilyClient 

def web_search(query : str,top_k : int = 3 ) -> str:
    ''' Search the web using current information using Tavily and filter highest similarity'''
    