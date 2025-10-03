import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

    client = Groq(api_key=GROQ_API_KEY)

settings = Settings()