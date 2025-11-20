const API_BASE_URL = 'http://localhost:8000';

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
    const response = await fetchWithAuth(`${API_BASE_URL}/api/analytics/dashboard`);
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
    const response = await fetchWithAuth(`${API_BASE_URL}/api/analytics/stats`);
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
    const token = localStorage.getItem('token');
  
    const res = await fetch(`${API_BASE_URL}/api/refresh-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      }
    });
  
    if (!res.ok) {
      throw new Error('Failed to refresh data');
    }
  
    return res.json();
  }
  
  // Product API functions
export async function getProducts() {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/products`);
    if (!response.ok) throw new Error('Failed to fetch products');
    return response.json();
  }
  
  export async function createProduct(productData) {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(productData),
    });
    if (!response.ok) throw new Error('Failed to create product');
    return response.json();
  }
  
  // Customer API functions
  export async function getCustomers() {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/customers`);
    if (!response.ok) throw new Error('Failed to fetch customers');
    return response.json();
  }
  
  export async function createCustomer(customerData) {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/customers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(customerData),
    });
    if (!response.ok) throw new Error('Failed to create customer');
    return response.json();
  }
  
  // Order API functions
  export async function getOrders() {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/orders`);
    if (!response.ok) throw new Error('Failed to fetch orders');
    return response.json();
  }
  
  export async function createOrder(orderData) {
    const response = await fetchWithAuth(`${API_BASE_URL}/api/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(orderData),
    });
    if (!response.ok) throw new Error('Failed to create order');
    return response.json();
  }