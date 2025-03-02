# filepath: /d:/Core App Development/Voice Agent/vagent/src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')