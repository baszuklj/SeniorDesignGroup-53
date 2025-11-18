import React, { useState } from 'react';
import UrlForm from './components/UrlForm';
import ResultsDisplay from './components/ResultsDisplay';
import LoadingSpinner from './components/LoadingSpinner';
import { verifyUrl } from './services/api';
import './styles/App.css';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUrlSubmit = async (url) => {
    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const data = await verifyUrl(url);
      setResults(data);
    } catch (err) {
      setError(err.message || 'An error occurred while verifying the URL');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>Link Reliability Checker</h1>
        <p>Verify the safety and reliability of any link in real-time with our comprehensive security scanner</p>
      </header>

      <main className="app-main">
        <UrlForm onSubmit={handleUrlSubmit} />
        
        {loading && <LoadingSpinner />}
        
        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}
        
        {results && <ResultsDisplay results={results} />}
      </main>

      <footer className="app-footer">
        <p>© 2025 Link Security Checker | Senior Design Group 54</p>
      </footer>
    </div>
  );
}

export default App;