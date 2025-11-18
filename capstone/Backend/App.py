from flask import Flask, request, jsonify
from flask_cors import CORS
from services.google_safe_browsing import GoogleSafeBrowsing
from services.virus_total import VirusTotal
from services.ssl_labs import SSLLabs
from services.phishtank import PhishTank
import os

app = Flask(__name__)
CORS(app)

# Initialize API clients
google_safe_browsing = GoogleSafeBrowsing()
virus_total = VirusTotal()
ssl_labs = SSLLabs()
phishtank = PhishTank()

@app.route('/api/verify-url', methods=['POST'])
def verify_url():
    try:
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Start all checks concurrently (in a real app, use async/await)
        results = {
            'google_safe_browsing': google_safe_browsing.check_url(url),
            'virus_total': virus_total.check_url(url),
            'ssl_labs': ssl_labs.check_ssl(url),
            'phishtank': phishtank.check_url(url)
        }
        
        # Calculate overall safety score
        safety_score = calculate_safety_score(results)
        results['safety_score'] = safety_score
        results['overall_verdict'] = get_verdict(safety_score)
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def calculate_safety_score(results):
    score = 100
    
    # Deduct points based on threats found
    if results['google_safe_browsing'].get('threats'):
        score -= 30
    
    if results['virus_total'].get('malicious_count', 0) > 0:
        score -= max(20, results['virus_total']['malicious_count'] * 5)
    
    if results['ssl_labs'].get('grade') in ['F', 'T']:
        score -= 25
    elif results['ssl_labs'].get('grade') in ['C', 'D']:
        score -= 15
    elif results['ssl_labs'].get('grade') == 'B':
        score -= 5
    
    if results['phishtank'].get('is_phishing'):
        score -= 40
    
    return max(0, score)

def get_verdict(score):
    if score >= 80:
        return 'Safe'
    elif score >= 60:
        return 'Moderately Safe'
    elif score >= 40:
        return 'Caution Advised'
    else:
        return 'Dangerous'

if __name__ == '__main__':
    app.run(debug=True, port=5000)
