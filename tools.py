from langchain_community.tools import DuckDuckGoSearchRun,WikipediaQueryRun
from langchain.tools import tool  
from langchain_community.utilities import WikipediaAPIWrapper
from datetime import datetime



@tool("save_text_to_file")
def save_tool(data: str, filename: str = "research_output.txt"):

    """CRITICAL: The 'data' argument must be a detailed, multi-line string 
    containing all the gathered facts, statistics, country breakdowns, 
    and conclusions formatted beautifully with clear headings. 
    Do not pass short summaries or conversational text here.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data successfully saved to {filename}"

# Initialize the underlying search engine
search = DuckDuckGoSearchRun()

# Define the custom tool using the modern decorator pattern
@tool("Search")
def search_tool(query: str) -> str:
    """Search the web for real-time information."""
    return search.run(query)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)


