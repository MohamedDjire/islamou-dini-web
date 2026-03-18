import { NavLink, useLocation } from 'react-router-dom'
import { 
  Home,
  BookOpen,
  Play,
  Users,
  Radio,
  MessageSquare,
  Heart,
  Clock,
  Bookmark,
  TrendingUp,
  Star,
  HelpCircle
} from 'lucide-react'
import { cn } from '../../lib/utils'
import { useAuth } from '../../context/AuthContext'

const mainNavItems = [
  { path: '/dashboard', icon: Home, label: 'Accueil' },
  { path: '/formations', icon: BookOpen, label: 'Formations' },
  { path: '/reels', icon: Play, label: 'Reels' },
  { path: '/communities', icon: Users, label: 'Communautes' },
  { path: '/lives', icon: Radio, label: 'Lives' },
  { path: '/messages', icon: MessageSquare, label: 'Messages' },
]

const libraryItems = [
  { path: '/my-formations', icon: Clock, label: 'En cours' },
  { path: '/favorites', icon: Heart, label: 'Favoris' },
  { path: '/bookmarks', icon: Bookmark, label: 'Sauvegardes' },
]

const discoverItems = [
  { path: '/trending', icon: TrendingUp, label: 'Tendances' },
  { path: '/popular', icon: Star, label: 'Populaires' },
]

export default function Sidebar({ isOpen, onClose }) {
  const location = useLocation()
  const { isAuthenticated } = useAuth()

  const NavItem = ({ item }) => {
    const isActive = location.pathname === item.path || 
                     (item.path !== '/dashboard' && location.pathname.startsWith(item.path))

    return (
      <NavLink
        to={item.path}
        onClick={onClose}
        className={cn(
          'flex items-center gap-3 px-4 py-2.5 rounded-lg font-medium transition-all duration-200',
          isActive
            ? 'bg-primary text-primary-foreground'
            : 'text-muted-foreground hover:text-foreground hover:bg-secondary'
        )}
      >
        <item.icon className={cn('h-5 w-5', isActive && 'text-primary-foreground')} />
        <span>{item.label}</span>
        {item.badge && (
          <span className="ml-auto bg-primary/20 text-primary text-xs px-2 py-0.5 rounded-full">
            {item.badge}
          </span>
        )}
      </NavLink>
    )
  }

  const SectionTitle = ({ children }) => (
    <h3 className="px-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
      {children}
    </h3>
  )

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-16 left-0 bottom-0 w-64 bg-card border-r border-border/50 z-40',
          'transform transition-transform duration-300 ease-in-out',
          'lg:translate-x-0 lg:static lg:z-0',
          isOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        <nav className="h-full overflow-y-auto py-6 px-3 space-y-6 scrollbar-hide">
          {/* Main Navigation */}
          <div className="space-y-1">
            {mainNavItems.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>

          {isAuthenticated && (
            <>
              {/* Divider decoratif */}
              <div className="divider-islamic">
                <span className="text-accent text-lg">&#10022;</span>
              </div>

              {/* Ma Bibliotheque */}
              <div className="space-y-1">
                <SectionTitle>Ma Bibliotheque</SectionTitle>
                {libraryItems.map((item) => (
                  <NavItem key={item.path} item={item} />
                ))}
              </div>
            </>
          )}

          {/* Divider decoratif */}
          <div className="divider-islamic">
            <span className="text-accent text-lg">&#10022;</span>
          </div>

          {/* Decouvrir */}
          <div className="space-y-1">
            <SectionTitle>Decouvrir</SectionTitle>
            {discoverItems.map((item) => (
              <NavItem key={item.path} item={item} />
            ))}
          </div>

          {/* Bottom section */}
          <div className="pt-4 mt-auto">
            <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-xl p-4 mx-1">
              <div className="flex items-center gap-2 mb-2">
                <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                  <Star className="h-4 w-4 text-primary" />
                </div>
                <span className="font-semibold text-foreground text-sm">Premium</span>
              </div>
              <p className="text-xs text-muted-foreground mb-3">
                Debloquez toutes les formations et fonctionnalites avancees
              </p>
              <button className="w-full py-2 bg-primary text-primary-foreground text-sm font-medium rounded-lg hover:bg-emerald-800 transition-colors">
                Passer Premium
              </button>
            </div>

            <NavLink
              to="/help"
              className="flex items-center gap-3 px-4 py-2.5 mt-4 text-muted-foreground hover:text-foreground hover:bg-secondary rounded-lg transition-colors"
            >
              <HelpCircle className="h-5 w-5" />
              Centre d'aide
            </NavLink>
          </div>
        </nav>
      </aside>
    </>
  )
}
