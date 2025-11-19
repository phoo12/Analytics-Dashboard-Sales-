const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper function to get auth token
function getToken() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
}

// Helper function for authenticated requests
async function fetchWithAuth(url, options = {}) {
  const token = getToken();
  
  if (!token) {
    throw new Error('No authentication token found');
  }

  const headers = {
    ...options.headers,
    'Authorization': `Bearer ${token}`,
  };

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // Token expired or invalid
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    throw new Error('Session expired. Please login again.');
  }

  return response;
}

export async function fetchAnalytics() {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/analytics`);
    if (!response.ok) {
      throw new Error('Failed to fetch analytics data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching analytics:', error);
    throw error;
  }
}

export async function fetchStats() {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/stats`);
    if (!response.ok) {
      throw new Error('Failed to fetch stats');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching stats:', error);
    throw error;
  }
}

export async function refreshData() {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/refresh-data`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to refresh data');
    }
    return await response.json();
  } catch (error) {
    console.error('Error refreshing data:', error);
    throw error;
  }
}