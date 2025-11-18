import requests
from config import Config

class PhishTank:
    def __init__(self):
        self.api_key = Config.PHISHTANK_API_KEY
        self.base_url = "http://checkurl.phishtank.com/checkurl/"
    
    def check_url(self, url):
        try:
            if not self.api_key:
                return {'error': 'PhishTank API key not configured'}
            
            payload = {
                'url': url,
                'format': 'json',
                'app_key': self.api_key
            }
            
            response = requests.post(self.base_url, data=payload)
            data = response.json()
            
            if 'results' in data:
                results = data['results']
                return {
                    'is_phishing': results.get('in_database', False),
                    'verified': results.get('verified', False),
                    'verified_at': results.get('verified_at'),
                    'message': 'Phishing database check completed'
                }
            else:
                return {'error': 'Invalid response from PhishTank'}
                
        except Exception as e:
            return {'error': f'PhishTank check failed: {str(e)}'}