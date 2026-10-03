import os
from google import genai
import dotenv

dotenv.load_dotenv(override=True)
api_key = os.environ.get("GEMINI_API_KEY")

print(f"Key loaded: {api_key[:10]}...")

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents="Say hello!"
    )
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
