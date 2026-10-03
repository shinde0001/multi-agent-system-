from pydantic import BaseModel, Field
from typing import List

class Reference(BaseModel):
    citation_id: int = Field(description="The number used in the text, e.g., 1")
    source_name: str = Field(description="Name of the publication/organization")
    title: str = Field(description="Title of the webpage/article")
    url: str = Field(description="Working URL link")

class ChapterDraft(BaseModel):
    content: str = Field(description="The markdown content of the chapter, including numbered citations like [1] and the 'Takeaway:' line. Do NOT include the reference list here.")
    references: List[Reference] = Field(description="List of references corresponding to citations")
