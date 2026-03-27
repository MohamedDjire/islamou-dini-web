/**
 * API Service for communicating with Django backend
 */

const API_BASE_URL = '/api';

/**
 * Get stored auth tokens
 */
export function getTokens() {
  const access = localStorage.getItem('access_token');
  const refresh = localStorage.getItem('refresh_token');
  return { access, refresh };
}

/**
 * Store auth tokens
 */
export function setTokens(access, refresh) {
  localStorage.setItem('access_token', access);
  localStorage.setItem('refresh_token', refresh);
}

/**
 * Clear auth tokens
 */
export function clearTokens() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
}

/**
 * Make authenticated API request
 */
async function apiRequest(endpoint, options = {}) {
  const { access } = getTokens();
  
  const headers = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (access) {
    headers['Authorization'] = `Bearer ${access}`;
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  // Handle token refresh if needed
  if (response.status === 401 && access) {
    const refreshed = await refreshToken();
    if (refreshed) {
      // Retry the request with new token
      const { access: newAccess } = getTokens();
      headers['Authorization'] = `Bearer ${newAccess}`;
      return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    } else {
      // Refresh failed, clear tokens
      clearTokens();
      throw new Error('Session expired');
    }
  }
  
  return response;
}

/**
 * Refresh the access token
 */
async function refreshToken() {
  const { refresh } = getTokens();
  if (!refresh) return false;
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh }),
    });
    
    if (response.ok) {
      const data = await response.json();
      setTokens(data.access, data.refresh || refresh);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

/**
 * Auth API
 */
export const authApi = {
  /**
   * Login user
   */
  async login(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/token/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    const data = await response.json();
    
    if (response.ok) {
      setTokens(data.access, data.refresh);
    }
    
    return { ok: response.ok, data };
  },
  
  /**
   * Register new user
   */
  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/users/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData),
    });
    
    const data = await response.json();
    return { ok: response.ok, data };
  },
  
  /**
   * Logout user
   */
  logout() {
    clearTokens();
  },
  
  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    const { access } = getTokens();
    return !!access;
  },
};

/**
 * Users API
 */
export const usersApi = {
  /**
   * Get current user profile
   */
  async getProfile() {
    const response = await apiRequest('/users/me/');
    const data = await response.json();
    return { ok: response.ok, data };
  },
  
  /**
   * Update current user profile
   */
  async updateProfile(userData) {
    const response = await apiRequest('/users/me/', {
      method: 'PATCH',
      body: JSON.stringify(userData),
    });
    const data = await response.json();
    return { ok: response.ok, data };
  },
  
  /**
   * Change password
   */
  async changePassword(passwords) {
    const response = await apiRequest('/users/change-password/', {
      method: 'PUT',
      body: JSON.stringify(passwords),
    });
    const data = await response.json();
    return { ok: response.ok, data };
  },
  
  /**
   * Get user by ID
   */
  async getUser(id) {
    const response = await apiRequest(`/users/${id}/`);
    const data = await response.json();
    return { ok: response.ok, data };
  },
  
  /**
   * List all users
   */
  async listUsers() {
    const response = await apiRequest('/users/');
    const data = await response.json();
    return { ok: response.ok, data };
  },
};

/**
 * Health check
 */
export async function healthCheck() {
  try {
    const response = await fetch(`${API_BASE_URL}/health/`);
    const data = await response.json();
    return { ok: response.ok, data };
  } catch (error) {
    return { ok: false, error: error.message };
  }
}

export default {
  auth: authApi,
  users: usersApi,
  healthCheck,
};
