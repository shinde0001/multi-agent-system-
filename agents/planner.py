import os
from .base_agent import BaseAgent
from models.brief import BookBrief
from models.outline import BookOutline

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        prompt_path = os.path.join(os.path.dirname(__file__), '..', 'prompts', 'planner_system.txt')
        with open(prompt_path, 'r') as f:
            self.system_instruction = f.read()
            
    def plan(self, brief: BookBrief) -> BookOutline:
        prompt = f"""
Book Title: {brief.title}
Audience: {brief.audience}
Tone: {brief.tone}
Length Instructions: {brief.length_instructions}
Citation Rules: {brief.citation_rules}

Please generate the 3-chapter outline based on these requirements.
"""
        return self.generate_structured(prompt, self.system_instruction, BookOutline)
