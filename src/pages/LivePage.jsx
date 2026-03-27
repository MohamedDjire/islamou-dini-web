import { Play, Users } from 'lucide-react';
import { Card, CardContent, Button } from '../components/ui';

export default function LivePage() {
  const lives = [
    {
      id: 1,
      title: 'Live: Questions-Réponses sur le Coran',
      host: 'Dr. Ahmed Hassan',
      viewers: 342,
      status: 'EN DIRECT',
    },
    {
      id: 2,
      title: 'Cours de Fiqh',
      host: 'Cheikh Mohamed',
      viewers: 0,
      status: 'À venir',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Sessions En Direct</h1>

      <div className="grid gap-6">
        {lives.map(live => (
          <Card key={live.id}>
            <CardContent className="pt-4">
              <div className="relative overflow-hidden bg-gray-900 rounded-lg mb-4 h-48 flex items-center justify-center">
                <Play size={64} className="text-white opacity-50" fill="white" />
                <div className="absolute top-3 left-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium text-white ${
                    live.status === 'EN DIRECT' ? 'bg-red-600' : 'bg-gray-600'
                  }`}>
                    {live.status}
                  </span>
                </div>
              </div>

              <h3 className="font-semibold text-lg text-gray-900 mb-2">{live.title}</h3>
              <p className="text-gray-600 mb-3">Hôte: {live.host}</p>

              {live.status === 'EN DIRECT' && (
                <div className="flex items-center gap-2 mb-4 text-red-600">
                  <Users size={16} />
                  {live.viewers} spectateurs
                </div>
              )}

              <Button className="w-full">
                {live.status === 'EN DIRECT' ? 'Regarder maintenant' : 'Rappel'}
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
