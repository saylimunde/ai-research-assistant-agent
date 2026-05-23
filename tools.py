from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import tool

# 1. Base instances
ddg_search = DuckDuckGoSearchRun()
wiki_wrapper = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())

# 2. Defensive Custom Wrappers with try-except blocks
@tool("search_tool")
def search_tool(query: str) -> str:
    """Searches the web for real-time information on a topic."""
    try:
        return ddg_search.run(query)
    except Exception as e:
        return f"Web search tool encountered a temporary error. Proceeding with research using alternative knowledge methods."

@tool("wiki_tool")
def wiki_tool(query: str) -> str:
    """Searches Wikipedia for historical, biographical, and statistical data."""
    try:
        return wiki_wrapper.run(query)
    except Exception as e:
        return f"Wikipedia search database returned an empty payload for '{query}'. Skipping direct wiki matching."

# 3. Save tool remains the same
@tool("save_tool")
def save_tool(content: str) -> str:
    """Saves the final generated research output report to a local text log."""
    try:
        filename = "research_output.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Report successfully persisted locally to {filename}"
    except Exception as e:
        return f"Error saving file: {str(e)}"
