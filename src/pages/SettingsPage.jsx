import { useState } from 'react';
import { Card, CardContent, CardHeader, Button, Input } from '../components/ui';
import { Bell, Lock, Eye, EyeOff } from 'lucide-react';

export default function SettingsPage() {
  const [showPassword, setShowPassword] = useState(false);

  return (
    <div className="max-w-2xl mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Paramètres</h1>

      {/* Notifications */}
      <Card>
        <CardHeader className="flex items-center gap-2">
          <Bell size={20} />
          Notifications
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <label className="text-gray-700">Notifications par email</label>
            <input type="checkbox" className="w-4 h-4" defaultChecked />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-gray-700">Notifications de formation</label>
            <input type="checkbox" className="w-4 h-4" defaultChecked />
          </div>
          <div className="flex items-center justify-between">
            <label className="text-gray-700">Notifications de communauté</label>
            <input type="checkbox" className="w-4 h-4" defaultChecked />
          </div>
        </CardContent>
      </Card>

      {/* Sécurité */}
      <Card>
        <CardHeader className="flex items-center gap-2">
          <Lock size={20} />
          Sécurité
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Ancien mot de passe</label>
            <div className="relative">
              <input type="password" className="w-full px-4 py-2 border border-gray-300 rounded-lg" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Nouveau mot de passe</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
              <button
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-2.5 text-gray-400"
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>
            </div>
          </div>
          <Button className="w-full">Changer le mot de passe</Button>
        </CardContent>
      </Card>
    </div>
  );
}
