import os
from .base_agent import BaseAgent
from models.brief import BookBrief
from models.outline import ChapterOutline
from models.research import ResearchDossier
from models.chapter import ChapterDraft
from typing import Optional

class WriterAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=0.7)
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'writer_system.txt')
        with open(prompt_path, 'r') as f:
            self.system_instruction = f.read()
            
    def write_chapter(self, brief: BookBrief, outline: ChapterOutline, dossier: ResearchDossier, previous_feedback: Optional[str] = None) -> ChapterDraft:
        prompt = f"""
Book Title: {brief.title}
Tone Rules: {brief.tone}
Citation Rules: {brief.citation_rules}

Chapter Title: {outline.title}
Themes to cover: {', '.join(outline.themes)}
Target Word Count: {outline.target_words} words.

RESEARCH DOSSIER (Use these facts and cite them!):
"""
        for i, source in enumerate(dossier.sources):
            prompt += f"- Fact {i+1}: {source.fact} (Source: {source.source_name}, URL: {source.source_url})\n"
            
        if previous_feedback:
            prompt += f"\n\nPREVIOUS EDITOR FEEDBACK TO FIX:\n{previous_feedback}\n"
            
        return self.generate_structured(prompt, self.system_instruction, ChapterDraft)
