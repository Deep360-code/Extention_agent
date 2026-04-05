from langchain_community.tools import TavilySearchResults, DuckDuckGoSearchRun
from langchain_core.tools import Tool
import os

def get_search_tool():
    """
    Returns a search tool. Prioritizes Tavily if API key is set, otherwise falls back to DuckDuckGo.
    """
    if os.getenv("TAVILY_API_KEY"):
        return TavilySearchResults()
    else:
        return DuckDuckGoSearchRun()

search_tool = get_search_tool()
