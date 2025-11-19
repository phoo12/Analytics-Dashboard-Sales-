const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function fetchAnalytics() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics`);
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
    const response = await fetch(`${API_BASE_URL}/api/stats`);
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
    const response = await fetch(`${API_BASE_URL}/api/refresh-data`, {
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