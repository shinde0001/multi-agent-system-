import os
from .base_agent import BaseAgent
from models.brief import BookBrief
from models.chapter import ChapterDraft
from models.review import EditResult

class EditorAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=0.2)
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'editor_system.txt')
        with open(prompt_path, 'r') as f:
            self.system_instruction = f.read()
            
    def review_chapter(self, brief: BookBrief, chapter: ChapterDraft) -> EditResult:
        prompt = f"""
Tone Rules: {brief.tone}
Citation Rules: {brief.citation_rules}
Target Length: {brief.length_instructions}

CHAPTER CONTENT:
{chapter.content}
"""
        return self.generate_structured(prompt, self.system_instruction, EditResult)
