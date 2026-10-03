import os
import dotenv
from google import genai
dotenv.load_dotenv(override=True)
client = genai.Client()
for m in client.models.list():
    if "flash" in m.name or "pro" in m.name:
        print(m.name)
