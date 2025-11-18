import requests
import time

class SSLLabs:
    def __init__(self):
        self.base_url = "https://api.ssllabs.com/api/v3/analyze"
    
    def check_ssl(self, url):
        try:
            # Extract domain from URL
            domain = self.extract_domain(url)
            if not domain:
                return {'error': 'Invalid domain'}
            
            # Start analysis
            start_response = requests.get(f"{self.base_url}?host={domain}&startNew=on")
            data = start_response.json()
            
            # Wait for analysis to complete (simplified - in production, use webhooks)
            max_attempts = 10
            for attempt in range(max_attempts):
                if data['status'] in ['READY', 'ERROR']:
                    break
                time.sleep(5)
                status_response = requests.get(f"{self.base_url}?host={domain}")
                data = status_response.json()
            
            if data['status'] == 'READY' and data.get('endpoints'):
                endpoint = data['endpoints'][0]
                return {
                    'grade': endpoint.get('grade', 'N/A'),
                    'has_warnings': endpoint.get('hasWarnings', False),
                    'protocols': [p['name'] for p in endpoint.get('details', {}).get('protocols', [])],
                    'message': f"SSL/TLS Grade: {endpoint.get('grade', 'N/A')}"
                }
            else:
                return {'error': 'SSL analysis not completed'}
                
        except Exception as e:
            return {'error': f'SSL Labs check failed: {str(e)}'}
    
    def extract_domain(self, url):
        """Extract domain from URL"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        return parsed.netloc or parsed.path.split('/')[0]