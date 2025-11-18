import requests
from config import Config

class VirusTotal:
    def __init__(self):
        self.api_key = Config.VIRUS_TOTAL_API_KEY
        self.base_url = "https://www.virustotal.com/vtapi/v2/url/report'"
    
    def check_url(self, url):
        try:
            if not self.api_key:
                return {'error': 'VirusTotal API key not configured'}
            
            # Submit URL for analysis
            headers = {
                'x-apikey': self.api_key
            }
            
            # First, submit the URL
            submit_response = requests.post(
                self.base_url,
                headers=headers,
                data={'url': url}
            )
            
            if submit_response.status_code == 200:
                analysis_id = submit_response.json()['data']['id']
                
                # Get the analysis results
                analysis_url = f"{self.base_url}/{analysis_id}"
                analysis_response = requests.get(analysis_url, headers=headers)
                
                if analysis_response.status_code == 200:
                    data = analysis_response.json()
                    attributes = data['data']['attributes']
                    
                    stats = attributes.get('stats', {})
                    return {
                        'malicious_count': stats.get('malicious', 0),
                        'suspicious_count': stats.get('suspicious', 0),
                        'harmless_count': stats.get('harmless', 0),
                        'undetected_count': stats.get('undetected', 0),
                        'reputation': attributes.get('reputation', 0),
                        'message': f"Scanned by {stats.get('total', 0)} engines"
                    }
            
            return {'error': 'Failed to analyze URL with VirusTotal'}
            
        except Exception as e:
            return {'error': f'VirusTotal check failed: {str(e)}'}