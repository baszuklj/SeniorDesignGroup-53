import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GOOGLE_SAFE_BROWSING_API_KEY = os.getenv('GOOGLE_SAFE_BROWSING_API_KEY')
    VIRUS_TOTAL_API_KEY = os.getenv('VIRUS_TOTAL_API_KEY')
    PHISHTANK_API_KEY = os.getenv('PHISHTANK_API_KEY')