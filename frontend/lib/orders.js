const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

function getToken() {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('access_token');
  }
  return null;
}

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
    if (typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
    }
    throw new Error('Session expired. Please login again.');
  }

  return response;
}

export async function fetchOrderDetail(orderId) {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/orders/${orderId}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch order details');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching order detail:', error);
    throw error;
  }
}

export async function fetchAllOrders(skip = 0, limit = 20) {
  try {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/orders?skip=${skip}&limit=${limit}`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch orders');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching orders:', error);
    throw error;
  }
}