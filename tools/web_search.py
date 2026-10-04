import time
from duckduckgo_search import DDGS
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_web(query: str, max_results: int = 5, retries: int = 3) -> List[Dict[str, str]]:
    """
    Search the web using DuckDuckGo.
    Returns a list of dicts with 'title', 'href', and 'body'.
    """
    for attempt in range(retries):
        try:
            logger.info(f"Searching web for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                return results
        except Exception as e:
            logger.warning(f"Search failed (attempt {attempt+1}/{retries}): {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    logger.error(f"Failed to search for query: {query} after {retries} attempts.")
    return []
