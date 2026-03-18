import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api'

// Instance Axios configuree
export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Intercepteur pour ajouter le token d'authentification
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Intercepteur pour gerer les erreurs et le refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    // Si erreur 401 et pas deja en train de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken,
          })

          const { token, refreshToken: newRefreshToken } = response.data

          localStorage.setItem('auth_token', token)
          localStorage.setItem('refresh_token', newRefreshToken)

          originalRequest.headers.Authorization = `Bearer ${token}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Si le refresh echoue, deconnecter l'utilisateur
        localStorage.removeItem('auth_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

// Fonctions utilitaires pour les requetes
export const apiGet = async (url, config = {}) => {
  const response = await api.get(url, config)
  return response.data
}

export const apiPost = async (url, data = {}, config = {}) => {
  const response = await api.post(url, data, config)
  return response.data
}

export const apiPut = async (url, data = {}, config = {}) => {
  const response = await api.put(url, data, config)
  return response.data
}

export const apiDelete = async (url, config = {}) => {
  const response = await api.delete(url, config)
  return response.data
}

// Fonction pour uploader des fichiers
export const uploadFile = async (file, endpoint = '/upload') => {
  const formData = new FormData()
  formData.append('file', file)

  const response = await api.post(endpoint, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })

  return response.data
}

export default api
