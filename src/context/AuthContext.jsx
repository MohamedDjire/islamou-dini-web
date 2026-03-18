import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { api } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)

  // Verifier l'authentification au chargement
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token')
      
      if (token) {
        try {
          const response = await api.get('/auth/me')
          setUser(response.data.user)
          setIsAuthenticated(true)
        } catch (error) {
          // Token invalide, nettoyer le storage
          localStorage.removeItem('auth_token')
          localStorage.removeItem('refresh_token')
          setUser(null)
          setIsAuthenticated(false)
        }
      }
      
      setIsLoading(false)
    }

    checkAuth()
  }, [])

  // Connexion
  const login = useCallback(async (email, password) => {
    try {
      const response = await api.post('/auth/login', { email, password })
      const { user: userData, token, refreshToken } = response.data

      localStorage.setItem('auth_token', token)
      localStorage.setItem('refresh_token', refreshToken)

      setUser(userData)
      setIsAuthenticated(true)

      return { success: true, user: userData }
    } catch (error) {
      const message = error.response?.data?.message || 'Erreur de connexion'
      return { success: false, error: message }
    }
  }, [])

  // Inscription
  const register = useCallback(async (userData) => {
    try {
      const response = await api.post('/auth/register', userData)
      const { user: newUser, token, refreshToken } = response.data

      localStorage.setItem('auth_token', token)
      localStorage.setItem('refresh_token', refreshToken)

      setUser(newUser)
      setIsAuthenticated(true)

      return { success: true, user: newUser }
    } catch (error) {
      const message = error.response?.data?.message || "Erreur d'inscription"
      return { success: false, error: message }
    }
  }, [])

  // Deconnexion
  const logout = useCallback(async () => {
    try {
      await api.post('/auth/logout')
    } catch (error) {
      // Ignorer les erreurs de logout
    } finally {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
      setUser(null)
      setIsAuthenticated(false)
    }
  }, [])

  // Mettre a jour le profil utilisateur
  const updateProfile = useCallback(async (profileData) => {
    try {
      const response = await api.put('/users/me', profileData)
      setUser(response.data.user)
      return { success: true, user: response.data.user }
    } catch (error) {
      const message = error.response?.data?.message || 'Erreur de mise a jour'
      return { success: false, error: message }
    }
  }, [])

  // Mot de passe oublie
  const forgotPassword = useCallback(async (email) => {
    try {
      await api.post('/auth/forgot-password', { email })
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.message || 'Erreur lors de la demande'
      return { success: false, error: message }
    }
  }, [])

  // Reinitialiser le mot de passe
  const resetPassword = useCallback(async (token, password) => {
    try {
      await api.post('/auth/reset-password', { token, password })
      return { success: true }
    } catch (error) {
      const message = error.response?.data?.message || 'Erreur de reinitialisation'
      return { success: false, error: message }
    }
  }, [])

  const value = {
    user,
    isLoading,
    isAuthenticated,
    login,
    register,
    logout,
    updateProfile,
    forgotPassword,
    resetPassword,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export default AuthContext
