import os
from .base_agent import BaseAgent
from models.chapter import ChapterDraft
from models.review import FactCheckResult, FactCheckItem
from tools.url_reader import read_url
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class FactCheckSingle(BaseModel):
    supported: bool
    notes: str

class FactCheckerAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=0.1) # low temp for strict fact checking
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'fact_checker_system.txt')
        with open(prompt_path, 'r') as f:
            self.system_instruction = f.read()
            
    def verify_citations(self, chapter: ChapterDraft) -> FactCheckResult:
        details = []
        failed_citations = []
        
        for ref in chapter.references:
            logger.info(f"Fact-checking citation [{ref.citation_id}] at {ref.url}")
            
            content = read_url(ref.url)
            
            if not content:
                logger.warning(f"Failed to access URL for citation [{ref.citation_id}]")
                details.append(FactCheckItem(
                    citation_id=ref.citation_id,
                    url_accessible=False,
                    claim_supported=False,
                    notes="URL was inaccessible or returned no main content."
                ))
                failed_citations.append(ref.citation_id)
                continue
                
            # URL accessible, now check the claim
            # We pass the chapter content and the reference to LLM
            prompt = f"Chapter Text:\n{chapter.content}\n\nCitation ID to verify: [{ref.citation_id}]\n\nSource Content from URL:\n{content[:5000]}"
            
            eval_result = self.generate_structured(prompt, self.system_instruction, FactCheckSingle)
            
            if not eval_result:
                # LLM failed to evaluate
                details.append(FactCheckItem(
                    citation_id=ref.citation_id,
                    url_accessible=True,
                    claim_supported=False,
                    notes="Failed to evaluate claim support."
                ))
                failed_citations.append(ref.citation_id)
                continue
                
            details.append(FactCheckItem(
                citation_id=ref.citation_id,
                url_accessible=True,
                claim_supported=eval_result.supported,
                notes=eval_result.notes
            ))
            
            if not eval_result.supported:
                failed_citations.append(ref.citation_id)
                
        status = 'approved' if len(failed_citations) == 0 else 'revision_needed'
        
        return FactCheckResult(
            status=status,
            failed_citations=failed_citations,
            details=details
        )
