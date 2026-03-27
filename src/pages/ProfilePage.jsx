import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, Button, Avatar } from '../components/ui';
import { Mail, MapPin, Calendar, Award } from 'lucide-react';

export default function ProfilePage() {
  const { user } = useAuth();

  if (!user) {
    return <div className="p-4">Chargement du profil...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      {/* Cover and Avatar */}
      <Card>
        <div className="h-32 bg-gradient-to-r from-primary to-secondary" />
        <CardContent className="pt-0">
          <div className="flex flex-col sm:flex-row gap-4 -mt-16 pb-6">
            <Avatar src={user.avatar} alt={user.username} size="xl" className="border-4 border-white" />
            <div className="flex-1 flex flex-col justify-end">
              <h1 className="text-2xl font-bold text-gray-900">{user.username}</h1>
              <p className="text-gray-600">{user.bio || 'Apprenant sur IslamouDini'}</p>
            </div>
            <Button>Modifier le profil</Button>
          </div>
        </CardContent>
      </Card>

      {/* Info Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-primary">5</div>
            <div className="text-sm text-gray-600">Formations</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-secondary">3</div>
            <div className="text-sm text-gray-600">Communautés</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-accent">12</div>
            <div className="text-sm text-gray-600">Certificats</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-primary">450</div>
            <div className="text-sm text-gray-600">Points XP</div>
          </CardContent>
        </Card>
      </div>

      {/* Details */}
      <Card>
        <CardHeader>Informations</CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center gap-3">
            <Mail size={20} className="text-gray-400" />
            <div>
              <div className="text-sm text-gray-600">Email</div>
              <div className="font-medium text-gray-900">{user.email}</div>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <Calendar size={20} className="text-gray-400" />
            <div>
              <div className="text-sm text-gray-600">Membre depuis</div>
              <div className="font-medium text-gray-900">Janvier 2024</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
