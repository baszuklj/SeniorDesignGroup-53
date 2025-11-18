import React from 'react';
import SafetyIndicator from './SafetyIndicator';

const ResultsDisplay = ({ results }) => {
  const {
    safety_score,
    overall_verdict,
    google_safe_browsing,
    virus_total,
    ssl_labs,
    phishtank
  } = results;

  return (
    <div className="results-display">
      <SafetyIndicator score={safety_score} verdict={overall_verdict} />
      
      <div className="results-grid">
        <div className="result-card">
          <h3>Google Safe Browsing</h3>
          {google_safe_browsing.error ? (
            <p className="error">{google_safe_browsing.error}</p>
          ) : (
            <>
              <div className={`status ${google_safe_browsing.is_safe ? 'safe' : 'dangerous'}`}>
                {google_safe_browsing.is_safe ? '✅ Safe' : '❌ Dangerous'}
              </div>
              <p>{google_safe_browsing.message}</p>
              {google_safe_browsing.threats && google_safe_browsing.threats.length > 0 && (
                <ul>
                  {google_safe_browsing.threats.map((threat, index) => (
                    <li key={index}>{threat}</li>
                  ))}
                </ul>
              )}
            </>
          )}
        </div>

        <div className="result-card">
          <h3>VirusTotal</h3>
          {virus_total.error ? (
            <p className="error">{virus_total.error}</p>
          ) : (
            <>
              <div className="status">
                {virus_total.malicious_count === 0 ? '✅ Clean' : `⚠️ ${virus_total.malicious_count} engines detected threats`}
              </div>
              <p>{virus_total.message}</p>
              <div className="stats">
                <span>Malicious: {virus_total.malicious_count}</span>
                <span>Suspicious: {virus_total.suspicious_count}</span>
                <span>Clean: {virus_total.harmless_count}</span>
              </div>
            </>
          )}
        </div>

        <div className="result-card">
          <h3>SSL Labs</h3>
          {ssl_labs.error ? (
            <p className="error">{ssl_labs.error}</p>
          ) : (
            <>
              <div className={`status grade-${ssl_labs.grade?.toLowerCase() || 'unknown'}`}>
                SSL Grade: {ssl_labs.grade || 'N/A'}
              </div>
              <p>{ssl_labs.message}</p>
              {ssl_labs.protocols && (
                <div>
                  <strong>Protocols:</strong> {ssl_labs.protocols.join(', ')}
                </div>
              )}
            </>
          )}
        </div>

        <div className="result-card">
          <h3>PhishTank</h3>
          {phishtank.error ? (
            <p className="error">{phishtank.error}</p>
          ) : (
            <>
              <div className={`status ${phishtank.is_phishing ? 'dangerous' : 'safe'}`}>
                {phishtank.is_phishing ? '❌ Phishing Site' : '✅ Not in Phishing Database'}
              </div>
              <p>{phishtank.message}</p>
              {phishtank.verified && (
                <p>Verified: {new Date(phishtank.verified_at).toLocaleDateString()}</p>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ResultsDisplay;