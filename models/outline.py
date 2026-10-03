from pydantic import BaseModel, Field
from typing import List

class ChapterOutline(BaseModel):
    title: str = Field(description="Title of the chapter")
    themes: List[str] = Field(description="Key themes to cover")
    target_words: int = Field(description="Target word count")
    data_points_needed: List[str] = Field(description="List of specific facts, figures, or dates to research")

class BookOutline(BaseModel):
    chapters: List[ChapterOutline] = Field(description="Exactly 3 chapters")
