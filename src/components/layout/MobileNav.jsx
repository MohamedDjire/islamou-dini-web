import { NavLink, useLocation } from 'react-router-dom'
import { Home, BookOpen, Play, Users, User } from 'lucide-react'
import { cn } from '../../lib/utils'

const navItems = [
  { path: '/dashboard', icon: Home, label: 'Accueil' },
  { path: '/formations', icon: BookOpen, label: 'Formations' },
  { path: '/reels', icon: Play, label: 'Reels' },
  { path: '/communities', icon: Users, label: 'Communautes' },
  { path: '/profile', icon: User, label: 'Profil' },
]

export default function MobileNav() {
  const location = useLocation()

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 lg:hidden bg-card border-t border-border/50 shadow-soft">
      <div className="flex items-center justify-around h-16 px-2">
        {navItems.map((item) => {
          const isActive = location.pathname === item.path || 
                          (item.path !== '/dashboard' && location.pathname.startsWith(item.path))

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={cn(
                'flex flex-col items-center justify-center gap-1 py-2 px-3 rounded-lg transition-colors',
                isActive
                  ? 'text-primary'
                  : 'text-muted-foreground hover:text-foreground'
              )}
            >
              <item.icon className={cn('h-5 w-5', isActive && 'text-primary')} />
              <span className="text-xs font-medium">{item.label}</span>
              {isActive && (
                <span className="absolute bottom-1 w-1 h-1 bg-primary rounded-full" />
              )}
            </NavLink>
          )
        })}
      </div>

      {/* Safe area pour iPhone */}
      <div className="h-safe-area-inset-bottom bg-card" />
    </nav>
  )
}
