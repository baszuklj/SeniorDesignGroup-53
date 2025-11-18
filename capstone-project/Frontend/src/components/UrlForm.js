import React, { useState } from 'react';

const UrlForm = ({ onSubmit }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      onSubmit(url.trim());
    }
  };

  return (
    <form className="url-form" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="url-input">Enter URL to verify:</label>
        <input
          id="url-input"
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com"
          required
        />
      </div>
      <button type="submit" className="verify-button">
        Verify URL
      </button>
    </form>
  );
};

export default UrlForm;