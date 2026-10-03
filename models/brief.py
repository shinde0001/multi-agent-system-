from pydantic import BaseModel

class BookBrief(BaseModel):
    title: str
    audience: str
    tone: str
    length_instructions: str
    citation_rules: str
