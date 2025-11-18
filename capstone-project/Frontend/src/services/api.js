const API_BASE_URL = 'http://localhost:5000';

export const verifyUrl = async (url) => {
  const response = await fetch(`${API_BASE_URL}/api/verify-url`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ url }),
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(errorData.error || 'Network response was not ok');
  }

  return response.json();
};