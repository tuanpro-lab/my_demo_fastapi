from tavily import TavilyClient 

def web_search(query : str) -> str:
    ''' Search the web using current information using Tavily'''
    results = tavily.search(query=query, max_results= 3 )
    output = []
    for r in results :
        output.append(f"- {r['title']}: {r['content'][:300]}")
    return "\n".join(output)