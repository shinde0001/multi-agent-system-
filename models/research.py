from pydantic import BaseModel, Field
from typing import List, Optional

class SourceEntry(BaseModel):
    data_point: str = Field(description="The original data point query")
    fact: str = Field(description="The verified fact or figure found")
    source_url: str = Field(description="URL where the fact was found")
    source_name: str = Field(description="Name of the publication or organization")
    article_title: str = Field(description="Title of the webpage/article")
    key_quote: str = Field(description="Verbatim quote supporting the fact")

class ResearchDossier(BaseModel):
    sources: List[SourceEntry] = Field(description="List of verified sources for the chapter")
