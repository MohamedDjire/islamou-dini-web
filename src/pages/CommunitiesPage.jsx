import { Link } from 'react-router-dom';
import { Users, MessageCircle, TrendingUp } from 'lucide-react';
import { Card, CardContent, Badge, Button, Avatar } from '../components/ui';

export default function CommunitiesPage() {
  const communities = [
    {
      id: 1,
      name: 'Étudiants en Tafsir',
      description: 'Communauté dédiée aux étudiants du Tafsir',
      image: '/placeholder.svg?height=100&width=100',
      members: 1230,
      posts: 456,
      category: 'Étude',
    },
    {
      id: 2,
      name: 'Fiqh Discussion',
      description: 'Discussions et débats sur les questions de Fiqh',
      image: '/placeholder.svg?height=100&width=100',
      members: 890,
      posts: 234,
      category: 'Discussion',
    },
  ];

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <h1 className="text-3xl font-bold text-gray-900">Communautés</h1>
      
      <div className="grid gap-6">
        {communities.map(community => (
          <Link key={community.id} to={`/communities/${community.id}`}>
            <Card className="hover:shadow-lg transition-shadow">
              <CardContent className="pt-4">
                <div className="flex gap-4">
                  <img src={community.image} alt={community.name} className="w-20 h-20 rounded-lg object-cover" />
                  <div className="flex-1">
                    <div className="flex items-start justify-between">
                      <div>
                        <h3 className="font-semibold text-lg text-gray-900">{community.name}</h3>
                        <p className="text-gray-600 text-sm mt-1">{community.description}</p>
                      </div>
                      <Badge variant="secondary">{community.category}</Badge>
                    </div>

                    <div className="flex gap-6 mt-4 text-sm text-gray-600">
                      <div className="flex items-center gap-2">
                        <Users size={16} />
                        {community.members} membres
                      </div>
                      <div className="flex items-center gap-2">
                        <MessageCircle size={16} />
                        {community.posts} posts
                      </div>
                    </div>

                    <Button className="mt-4" size="sm">
                      Rejoindre
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
