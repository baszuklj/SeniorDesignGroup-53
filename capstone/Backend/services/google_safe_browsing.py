import requests
import hashlib
import json
from config import Config

class GoogleSafeBrowsing:
    def __init__(self):
        self.api_key = Config.GOOGLE_SAFE_BROWSING_API_KEY
        self.url = "https://safebrowsing.googleapis.com/v4/threatMatches:find"
    
    def check_url(self, url):
        try:
            if not self.api_key:
                return {'error': 'Google Safe Browsing API key not configured'}
            
            payload = {
                "client": {
                    "clientId": "url-verifier",
                    "clientVersion": "1.0.0"
                },
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url}]
                }
            }
            
            params = {'key': self.api_key}
            response = requests.post(self.url, params=params, json=payload)
            data = response.json()
            
            if 'matches' in data:
                threats = [match['threatType'] for match in data['matches']]
                return {
                    'is_safe': False,
                    'threats': threats,
                    'message': f'Website identified as dangerous: {", ".join(threats)}'
                }
            else:
                return {
                    'is_safe': True,
                    'threats': [],
                    'message': 'No threats found via Google Safe Browsing'
                }
                
        except Exception as e:
            return {'error': f'Google Safe Browsing check failed: {str(e)}'}