import React from 'react';

const LoadingSpinner = () => {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p>Verifying URL security...</p>
      <p className="loading-subtext">Checking multiple security services</p>
    </div>
  );
};

export default LoadingSpinner;