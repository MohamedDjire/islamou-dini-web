import { Link, useLocation } from 'react-router-dom';
import { Home, BookOpen, Users, Video, MessageSquare, Settings, LogOut, X } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';

const navItems = [
  { icon: Home, label: 'Accueil', path: '/' },
  { icon: BookOpen, label: 'Formations', path: '/formations' },
  { icon: Users, label: 'Communautés', path: '/communities' },
  { icon: Video, label: 'Reels', path: '/reels' },
  { icon: MessageSquare, label: 'Messages', path: '/messages', auth: true },
  { icon: Settings, label: 'Paramètres', path: '/settings', auth: true },
];

export default function Sidebar({ isOpen, onClose }) {
  const { user } = useAuth();
  const location = useLocation();
  
  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 lg:hidden z-40"
          onClick={onClose}
        />
      )}
      
      {/* Sidebar */}
      <aside className={`fixed lg:static left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 flex flex-col z-40 transition-transform duration-300 lg:translate-x-0 ${
        isOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        {/* Close button for mobile */}
        <div className="lg:hidden flex justify-end p-4">
          <button onClick={onClose} className="text-gray-600 hover:text-gray-900">
            <X size={24} />
          </button>
        </div>
        
        {/* Navigation */}
        <nav className="flex-1 px-4 py-4">
          <div className="space-y-2">
            {navItems.map((item) => {
              if (item.auth && !user) return null;
              
              const isActive = location.pathname === item.path;
              const Icon = item.icon;
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={onClose}
                  className={`flex items-center gap-3 px-4 py-2 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-primary text-white'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              );
            })}
          </div>
        </nav>
        
        {/* User section */}
        {user && (
          <div className="border-t border-gray-200 p-4">
            <button className="w-full flex items-center gap-3 text-gray-700 hover:text-gray-900 py-2">
              <LogOut size={20} />
              <span className="font-medium">Déconnexion</span>
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
