import os
from .base_agent import BaseAgent
from models.outline import ChapterOutline
from models.research import ResearchDossier, SourceEntry
from tools.web_search import search_web
from tools.url_reader import read_url
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class FactExtractionResult(BaseModel):
    found: bool
    fact: str = ""
    key_quote: str = ""

class ResearcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=0.3) # lower temp for facts
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'researcher_system.txt')
        with open(prompt_path, 'r') as f:
            self.system_instruction = f.read()
            
    def research_chapter(self, chapter_outline: ChapterOutline) -> ResearchDossier:
        sources = []
        for data_point in chapter_outline.data_points_needed:
            logger.info(f"Researching: {data_point}")
            
            # Step 1: Search the web
            search_results = search_web(data_point, max_results=7)
            
            fact_found = False
            for res in search_results:
                url = res.get('href')
                title = res.get('title', '')
                if not url: continue
                
                # Step 2: Read URL content
                content = read_url(url)
                if not content: continue
                
                # Step 3: Use LLM to extract fact
                prompt = f"Data Point Needed: {data_point}\n\nSource URL: {url}\nSource Title: {title}\n\nContent:\n{content[:15000]}" # Tripled context length to ensure we don't miss facts at the bottom of pages
                
                extracted = self.generate_structured(prompt, self.system_instruction, FactExtractionResult)
                
                if extracted and extracted.found:
                    source_entry = SourceEntry(
                        data_point=data_point,
                        fact=extracted.fact,
                        source_url=url,
                        source_name=url.split('/')[2] if '//' in url else "Web Source",
                        article_title=title,
                        key_quote=extracted.key_quote
                    )
                    sources.append(source_entry)
                    fact_found = True
                    break # move to next data point
            
            if not fact_found:
                logger.info(f"Fallback: Searching Wikipedia for: {data_point}")
                wiki_results = search_web(f"{data_point} site:wikipedia.org", max_results=3)
                for res in wiki_results:
                    url = res.get('href')
                    if not url: continue
                    content = read_url(url)
                    if not content: continue
                    
                    prompt = f"Data Point Needed: {data_point}\n\nSource URL: {url}\nSource Title: {res.get('title', '')}\n\nContent:\n{content[:15000]}"
                    extracted = self.generate_structured(prompt, self.system_instruction, FactExtractionResult)
                    
                    if extracted and extracted.found:
                        source_entry = SourceEntry(
                            data_point=data_point,
                            fact=extracted.fact,
                            source_url=url,
                            source_name="Wikipedia",
                            article_title=res.get('title', ''),
                            key_quote=extracted.key_quote
                        )
                        sources.append(source_entry)
                        fact_found = True
                        break

            if not fact_found:
                logger.warning(f"Could not find verified fact for: {data_point}")
                
        return ResearchDossier(sources=sources)
