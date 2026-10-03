from pydantic import BaseModel, Field
from typing import List, Optional

class EditResult(BaseModel):
    status: str = Field(description="Must be 'approved' or 'revision_needed'")
    feedback: List[str] = Field(description="List of specific improvements needed if revision_needed. Empty if approved.")

class FactCheckItem(BaseModel):
    citation_id: int = Field(description="The citation number, e.g., 1")
    url_accessible: bool = Field(description="True if the URL loads and contains text")
    claim_supported: bool = Field(description="True if the source actually supports the claim in the text")
    notes: str = Field(description="Explanation of why it passed or failed")

class FactCheckResult(BaseModel):
    status: str = Field(description="Must be 'approved' or 'revision_needed'")
    failed_citations: List[int] = Field(description="List of citation_ids that failed verification")
    details: List[FactCheckItem] = Field(description="Detailed verification results for every citation")
