import os
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from google import genai
from google.genai import types
import dotenv
import logging
import time

dotenv.load_dotenv(override=True)
logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

_last_call_time = 0.0
_MIN_DELAY_SECONDS = 15

class BaseAgent:
    """Base class for all agents to handle LLM communication via Gemini."""
    def __init__(self, model_name: str = "gemini-3.5-flash-lite", temperature: float = 0.7):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name
        self.temperature = temperature

    def _rate_limit(self):
        global _last_call_time
        now = time.time()
        elapsed = now - _last_call_time
        if elapsed < _MIN_DELAY_SECONDS:
            wait = _MIN_DELAY_SECONDS - elapsed
            time.sleep(wait)
        _last_call_time = time.time()

    def generate_structured(self, prompt: str, system_instruction: str, response_schema: Type[T], max_retries: int = 4) -> Optional[T]:
        """Calls the Gemini model and forces the output to match the Pydantic schema."""
        config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=response_schema,
            system_instruction=system_instruction,
            temperature=self.temperature
        )

        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                
                json_str = response.text
                parsed = response_schema.model_validate_json(json_str)
                return parsed
                
            except Exception as e:
                logger.warning(f"LLM generation failed (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(min(30 * (2 ** attempt), 120))
                
        logger.error(f"Failed to generate structured output after {max_retries} attempts.")
        return None
        
    def generate_text(self, prompt: str, system_instruction: str, max_retries: int = 4) -> Optional[str]:
        """Calls the Gemini model for unstructured text output."""
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=self.temperature
        )

        for attempt in range(max_retries):
            try:
                self._rate_limit()
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=config
                )
                return response.text
            except Exception as e:
                logger.warning(f"LLM generation failed (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(min(30 * (2 ** attempt), 120))
                
        return None
