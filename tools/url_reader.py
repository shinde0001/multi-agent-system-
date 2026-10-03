import trafilatura
import logging

logger = logging.getLogger(__name__)

def read_url(url: str, timeout: int = 10) -> str:
    """
    Fetches the HTML of a URL and extracts the main article text using trafilatura.
    Returns the extracted text, or an empty string if it fails.
    """
    try:
        logger.info(f"Fetching URL: {url}")
        # trafilatura fetch handles User-Agent, timeouts, and basic anti-bot internally
        downloaded = trafilatura.fetch_url(url)
        if downloaded is None:
            logger.warning(f"Failed to fetch HTML for: {url}")
            return ""
        
        # Extract main text
        text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
        if text:
            return text
        else:
            logger.warning(f"Could not extract main content from: {url}")
            return ""
    except Exception as e:
        logger.warning(f"Error reading URL {url}: {e}")
        return ""
