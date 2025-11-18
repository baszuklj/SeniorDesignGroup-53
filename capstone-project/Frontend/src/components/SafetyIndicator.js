import React from 'react';

const SafetyIndicator = ({ score, verdict }) => {
  const getScoreColor = (score) => {
    if (score >= 80) return '#4CAF50';
    if (score >= 60) return '#FFC107';
    if (score >= 40) return '#FF9800';
    return '#F44336';
  };

  const getVerdictColor = (verdict) => {
    switch (verdict) {
      case 'Safe': return '#4CAF50';
      case 'Moderately Safe': return '#FFC107';
      case 'Caution Advised': return '#FF9800';
      case 'Dangerous': return '#F44336';
      default: return '#757575';
    }
  };

  return (
    <div className="safety-indicator">
      <div className="score-display">
        <div className="score-circle">
          <svg width="120" height="120" viewBox="0 0 120 120">
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke="#e0e0e0"
              strokeWidth="8"
            />
            <circle
              cx="60"
              cy="60"
              r="54"
              fill="none"
              stroke={getScoreColor(score)}
              strokeWidth="8"
              strokeDasharray={`${(score / 100) * 339.292} 339.292`}
              transform="rotate(-90 60 60)"
            />
            <text
              x="60"
              y="60"
              textAnchor="middle"
              dy="7"
              fontSize="20"
              fontWeight="bold"
              fill={getScoreColor(score)}
            >
              {score}
            </text>
          </svg>
        </div>
        <div className="verdict" style={{ color: getVerdictColor(verdict) }}>
          {verdict}
        </div>
      </div>
    </div>
  );
};

export default SafetyIndicator;