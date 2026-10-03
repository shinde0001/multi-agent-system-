from pydantic import BaseModel

class BookBrief(BaseModel):
    title: str
    audience: str
    tone: str
    length_instructions: str
    citation_rules: str

# Our default brief from the assignment
DEFAULT_BRIEF = BookBrief(
    title="Pay Me on UPI: How Digital Payments Changed Small Business in India",
    audience="First-time small-business owners in India",
    tone="Friendly, clear and encouraging, as if a mentor is explaining things to a new shop owner. Plain English with no jargon; explain any technical term the first time it appears. The same tone and voice across all three chapters.",
    length_instructions="3 chapters, about 600-900 words each.",
    citation_rules="Every fact, figure and date must have a numbered citation in the text, for example [1]. Each chapter ends with a reference list giving the source name, title and a working link. Prefer official sources (NPCI, RBI, gov) and reputable news. Each chapter ends with one line starting with 'Takeaway:', placed before its reference list."
)

MAX_REVISIONS = 2
MODEL_NAME = "gemini-3.5-flash-lite"
