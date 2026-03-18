import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { 
  Search, 
  Bell, 
  MessageSquare, 
  Menu, 
  X,
  User,
  Settings,
  LogOut,
  ChevronDown
} from 'lucide-react'
import { cn } from '../../lib/utils'
import { useAuth } from '../../context/AuthContext'
import { Button, Avatar } from '../ui'

export default function Header({ onMenuClick, isSidebarOpen }) {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const [searchQuery, setSearchQuery] = useState('')
  const [showUserMenu, setShowUserMenu] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)

  const handleSearch = (e) => {
    e.preventDefault()
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`)
    }
  }

  const handleLogout = async () => {
    await logout()
    navigate('/login')
  }

  // Notifications simulees
  const notifications = [
    { id: 1, title: 'Nouvelle formation disponible', message: 'Decouvrez notre nouvelle formation sur le Tajwid', time: 'Il y a 5 min', unread: true },
    { id: 2, title: 'Session de lecture', message: 'Votre session commence dans 1 heure', time: 'Il y a 30 min', unread: true },
    { id: 3, title: 'Message recu', message: 'Sheikh Ahmad vous a envoye un message', time: 'Il y a 2h', unread: false },
  ]

  const unreadCount = notifications.filter(n => n.unread).length

  return (
    <header className="sticky top-0 z-40 w-full bg-card border-b border-border/50 shadow-soft">
      <div className="flex items-center justify-between h-16 px-4 lg:px-6">
        {/* Left: Menu & Logo */}
        <div className="flex items-center gap-3">
          <button
            onClick={onMenuClick}
            className="lg:hidden p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
            aria-label={isSidebarOpen ? 'Fermer le menu' : 'Ouvrir le menu'}
          >
            {isSidebarOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
          </button>

          <Link to="/" className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-gradient-emerald flex items-center justify-center">
              <span className="text-white font-serif font-bold text-lg">I</span>
            </div>
            <span className="hidden sm:block font-serif font-semibold text-xl text-foreground">
              Islamou<span className="text-primary">Dini</span>
            </span>
          </Link>
        </div>

        {/* Center: Search */}
        <form 
          onSubmit={handleSearch}
          className="hidden md:flex flex-1 max-w-md mx-8"
        >
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="search"
              placeholder="Rechercher formations, formateurs..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-2 rounded-full bg-secondary border-none text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/20"
            />
          </div>
        </form>

        {/* Right: Actions */}
        <div className="flex items-center gap-2">
          {/* Mobile search */}
          <button 
            onClick={() => navigate('/search')}
            className="md:hidden p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
          >
            <Search className="h-5 w-5" />
          </button>

          {isAuthenticated ? (
            <>
              {/* Messages */}
              <Link
                to="/messages"
                className="relative p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
              >
                <MessageSquare className="h-5 w-5" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-primary rounded-full" />
              </Link>

              {/* Notifications */}
              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="relative p-2 rounded-lg text-muted-foreground hover:text-foreground hover:bg-secondary transition-colors"
                >
                  <Bell className="h-5 w-5" />
                  {unreadCount > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 w-5 h-5 bg-primary text-primary-foreground text-xs rounded-full flex items-center justify-center font-medium">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {/* Dropdown notifications */}
                {showNotifications && (
                  <>
                    <div 
                      className="fixed inset-0 z-40" 
                      onClick={() => setShowNotifications(false)} 
                    />
                    <div className="absolute right-0 mt-2 w-80 bg-card rounded-xl border border-border shadow-elevated z-50 overflow-hidden">
                      <div className="p-4 border-b border-border">
                        <h3 className="font-semibold text-foreground">Notifications</h3>
                      </div>
                      <div className="max-h-80 overflow-y-auto">
                        {notifications.map((notif) => (
                          <div
                            key={notif.id}
                            className={cn(
                              'p-4 border-b border-border/50 hover:bg-secondary/50 cursor-pointer transition-colors',
                              notif.unread && 'bg-primary/5'
                            )}
                          >
                            <div className="flex items-start gap-3">
                              {notif.unread && (
                                <span className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0" />
                              )}
                              <div className={cn(!notif.unread && 'ml-5')}>
                                <p className="font-medium text-sm text-foreground">{notif.title}</p>
                                <p className="text-sm text-muted-foreground mt-0.5">{notif.message}</p>
                                <p className="text-xs text-muted-foreground mt-1">{notif.time}</p>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                      <Link
                        to="/notifications"
                        className="block p-3 text-center text-sm text-primary hover:bg-secondary/50 transition-colors"
                        onClick={() => setShowNotifications(false)}
                      >
                        Voir toutes les notifications
                      </Link>
                    </div>
                  </>
                )}
              </div>

              {/* User Menu */}
              <div className="relative ml-2">
                <button
                  onClick={() => setShowUserMenu(!showUserMenu)}
                  className="flex items-center gap-2 p-1.5 rounded-lg hover:bg-secondary transition-colors"
                >
                  <Avatar 
                    src={user?.avatar} 
                    name={`${user?.firstName} ${user?.lastName}`}
                    size="sm"
                  />
                  <ChevronDown className={cn(
                    'h-4 w-4 text-muted-foreground transition-transform hidden sm:block',
                    showUserMenu && 'rotate-180'
                  )} />
                </button>

                {/* Dropdown user */}
                {showUserMenu && (
                  <>
                    <div 
                      className="fixed inset-0 z-40" 
                      onClick={() => setShowUserMenu(false)} 
                    />
                    <div className="absolute right-0 mt-2 w-56 bg-card rounded-xl border border-border shadow-elevated z-50 overflow-hidden">
                      <div className="p-4 border-b border-border">
                        <p className="font-medium text-foreground">{user?.firstName} {user?.lastName}</p>
                        <p className="text-sm text-muted-foreground">{user?.email}</p>
                      </div>
                      <div className="p-2">
                        <Link
                          to="/profile"
                          onClick={() => setShowUserMenu(false)}
                          className="flex items-center gap-3 px-3 py-2 rounded-lg text-foreground hover:bg-secondary transition-colors"
                        >
                          <User className="h-4 w-4" />
                          Mon profil
                        </Link>
                        <Link
                          to="/settings"
                          onClick={() => setShowUserMenu(false)}
                          className="flex items-center gap-3 px-3 py-2 rounded-lg text-foreground hover:bg-secondary transition-colors"
                        >
                          <Settings className="h-4 w-4" />
                          Parametres
                        </Link>
                        <hr className="my-2 border-border" />
                        <button
                          onClick={handleLogout}
                          className="flex items-center gap-3 w-full px-3 py-2 rounded-lg text-red-600 hover:bg-red-50 transition-colors"
                        >
                          <LogOut className="h-4 w-4" />
                          Deconnexion
                        </button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Button 
                variant="ghost" 
                size="sm"
                onClick={() => navigate('/login')}
              >
                Connexion
              </Button>
              <Button 
                size="sm"
                onClick={() => navigate('/register')}
              >
                S'inscrire
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
