import { Link } from 'react-router-dom';
import { Menu, Search, Bell, MessageCircle } from 'lucide-react';
import { Avatar, Button } from '../ui';
import { useAuth } from '../../contexts/AuthContext';

export default function Header({ onMenuToggle }) {
  const { user, logout } = useAuth();
  
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
      <div className="flex items-center justify-between px-4 py-3 max-w-7xl mx-auto">
        {/* Logo and Menu */}
        <div className="flex items-center gap-4">
          <button onClick={onMenuToggle} className="lg:hidden text-gray-600 hover:text-gray-900">
            <Menu size={24} />
          </button>
          <Link to="/" className="flex items-center gap-2 font-bold text-xl text-primary">
            <div className="w-8 h-8 bg-gradient-to-br from-primary to-secondary rounded-lg" />
            IslamouDini
          </Link>
        </div>
        
        {/* Search Bar */}
        <div className="hidden md:flex flex-1 max-w-md mx-8">
          <div className="relative w-full">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={18} />
            <input 
              type="text"
              placeholder="Chercher..."
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            />
          </div>
        </div>
        
        {/* Right Actions */}
        <div className="flex items-center gap-4">
          {user ? (
            <>
              <button className="relative text-gray-600 hover:text-gray-900 transition-colors">
                <Bell size={20} />
                <span className="absolute top-0 right-0 w-2 h-2 bg-red-500 rounded-full" />
              </button>
              <button className="relative text-gray-600 hover:text-gray-900 transition-colors">
                <MessageCircle size={20} />
              </button>
              <div className="flex items-center gap-2 ml-4 pl-4 border-l border-gray-200">
                <Avatar src={user.avatar} alt={user.username} size="sm" />
                <div className="hidden sm:block">
                  <p className="text-sm font-medium text-gray-900">{user.username}</p>
                </div>
                <Button 
                  variant="ghost" 
                  size="sm"
                  onClick={logout}
                >
                  Déconnexion
                </Button>
              </div>
            </>
          ) : (
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Link to="/login">Connexion</Link>
              </Button>
              <Button size="sm">
                <Link to="/register">S&apos;inscrire</Link>
              </Button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
}
