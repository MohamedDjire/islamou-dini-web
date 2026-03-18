import { useState } from 'react'
import { Outlet } from 'react-router-dom'
import Header from '../components/layout/Header'
import Sidebar from '../components/layout/Sidebar'
import MobileNav from '../components/layout/MobileNav'
import { useAuth } from '../context/AuthContext'

export default function MainLayout() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false)
  const { isAuthenticated } = useAuth()

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen)
  const closeSidebar = () => setIsSidebarOpen(false)

  return (
    <div className="min-h-screen bg-background islamic-pattern-bg">
      {/* Header */}
      <Header 
        onMenuClick={toggleSidebar} 
        isSidebarOpen={isSidebarOpen} 
      />

      <div className="flex">
        {/* Sidebar - visible seulement pour les utilisateurs connectes */}
        {isAuthenticated && (
          <Sidebar 
            isOpen={isSidebarOpen} 
            onClose={closeSidebar} 
          />
        )}

        {/* Main Content */}
        <main className={`flex-1 min-h-[calc(100vh-4rem)] ${isAuthenticated ? 'lg:ml-0' : ''}`}>
          <div className="container-app py-6 pb-24 lg:pb-6">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Mobile Navigation - visible seulement pour les utilisateurs connectes */}
      {isAuthenticated && <MobileNav />}
    </div>
  )
}
