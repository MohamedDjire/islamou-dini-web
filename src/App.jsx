import { useState, useEffect } from 'react'
import { AuthProvider } from './contexts/AuthContext'
import { healthCheck } from './services/api'
import './App.css'

function AppContent() {
  const [backendStatus, setBackendStatus] = useState('checking')
  const [backendInfo, setBackendInfo] = useState(null)

  useEffect(() => {
    checkBackend()
  }, [])

  async function checkBackend() {
    const result = await healthCheck()
    if (result.ok) {
      setBackendStatus('connected')
      setBackendInfo(result.data)
    } else {
      setBackendStatus('error')
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Islamou Dini</h1>
        <p>Application avec Django Backend</p>
      </header>

      <main className="app-main">
        <section className="status-card">
          <h2>Status du Backend Django</h2>
          
          {backendStatus === 'checking' && (
            <div className="status checking">
              <span className="status-dot"></span>
              Verification de la connexion...
            </div>
          )}
          
          {backendStatus === 'connected' && (
            <div className="status connected">
              <span className="status-dot"></span>
              Backend connecte
              {backendInfo && (
                <pre className="backend-info">
                  {JSON.stringify(backendInfo, null, 2)}
                </pre>
              )}
            </div>
          )}
          
          {backendStatus === 'error' && (
            <div className="status error">
              <span className="status-dot"></span>
              Backend non disponible
              <button onClick={checkBackend} className="retry-btn">
                Reessayer
              </button>
            </div>
          )}
        </section>

        <section className="api-info">
          <h2>API Endpoints Django</h2>
          <ul>
            <li><code>GET /api/health/</code> - Health check</li>
            <li><code>POST /api/auth/token/</code> - Login (JWT)</li>
            <li><code>POST /api/auth/token/refresh/</code> - Refresh token</li>
            <li><code>POST /api/users/register/</code> - Register</li>
            <li><code>GET /api/users/me/</code> - Current user profile</li>
            <li><code>PATCH /api/users/me/</code> - Update profile</li>
            <li><code>PUT /api/users/change-password/</code> - Change password</li>
            <li><code>GET /api/admin/</code> - Django Admin</li>
          </ul>
        </section>
      </main>
    </div>
  )
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  )
}

export default App
