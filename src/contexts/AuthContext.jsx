/**
 * Authentication Context for managing user state
 */

import { createContext, useContext, useState, useEffect } from 'react';
import { authApi, usersApi, getTokens } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check authentication on mount
  useEffect(() => {
    checkAuth();
  }, []);

  async function checkAuth() {
    const { access } = getTokens();
    if (access) {
      try {
        const { ok, data } = await usersApi.getProfile();
        if (ok) {
          setUser(data);
        } else {
          authApi.logout();
        }
      } catch {
        authApi.logout();
      }
    }
    setLoading(false);
  }

  async function login(email, password) {
    setError(null);
    try {
      const { ok, data } = await authApi.login(email, password);
      if (ok) {
        // Fetch user profile after login
        const profileResult = await usersApi.getProfile();
        if (profileResult.ok) {
          setUser(profileResult.data);
        }
        return true;
      } else {
        const message = data.detail || 'Email ou mot de passe incorrect';
        setError(message);
        return false;
      }
    } catch (err) {
      const message = err.message || 'Erreur de connexion';
      setError(message);
      return false;
    }
  }

  async function register(username, email, password) {
    setError(null);
    try {
      const { ok, data } = await authApi.register({ username, email, password });
      if (ok) {
        // Auto-login after registration
        const loginResult = await login(email, password);
        return loginResult;
      } else {
        const message = Object.values(data).flat().join(', ') || 'Erreur d\'inscription';
        setError(message);
        return false;
      }
    } catch (err) {
      const message = err.message || 'Erreur d\'inscription';
      setError(message);
      return false;
    }
  }

  function logout() {
    authApi.logout();
    setUser(null);
    setError(null);
  }

  async function updateProfile(userData) {
    try {
      const { ok, data } = await usersApi.updateProfile(userData);
      if (ok) {
        setUser(data);
        return { success: true };
      }
      return { success: false, error: 'Erreur de mise a jour' };
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  const value = {
    user,
    loading,
    error,
    isAuthenticated: !!user,
    login,
    register,
    logout,
    updateProfile,
    clearError: () => setError(null),
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export default AuthContext;
