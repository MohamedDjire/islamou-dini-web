import { Card, CardContent, CardHeader } from '../components/ui';
import { Users, BookOpen, AlertCircle, TrendingUp } from 'lucide-react';

export default function AdminPage() {
  const stats = [
    { icon: Users, label: 'Utilisateurs', value: '10,234' },
    { icon: BookOpen, label: 'Formations', value: '542' },
    { icon: AlertCircle, label: 'Signalements', value: '23' },
    { icon: TrendingUp, label: 'Croissance', value: '+12%' },
  ];

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Tableau de bord Admin</h1>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {stats.map(stat => {
          const Icon = stat.icon;
          return (
            <Card key={stat.label}>
              <CardContent className="pt-6">
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-lg flex items-center justify-center">
                    <Icon className="text-primary" size={24} />
                  </div>
                  <div>
                    <div className="text-sm text-gray-600">{stat.label}</div>
                    <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Recent Reports */}
      <Card>
        <CardHeader>Signalements récents</CardHeader>
        <CardContent>
          <p className="text-gray-600">Aucun signalement pour le moment</p>
        </CardContent>
      </Card>

      {/* User Management */}
      <Card>
        <CardHeader>Gestion des utilisateurs</CardHeader>
        <CardContent>
          <p className="text-gray-600">Accédez au <a href="/admin/" className="text-primary hover:underline">panel d&apos;administration Django</a></p>
        </CardContent>
      </Card>
    </div>
  );
}
