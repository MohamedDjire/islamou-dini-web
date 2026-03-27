import { useParams } from 'react-router-dom';
import { MessageCircle, Users, Share2 } from 'lucide-react';
import { Card, CardContent, Button, Avatar } from '../components/ui';

export default function CommunityPage() {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <div className="bg-gradient-to-r from-primary to-secondary text-white p-8 rounded-lg">
        <h1 className="text-3xl font-bold">Communauté #{id}</h1>
        <p className="mt-2 opacity-90">Rejoignez notre communauté d&apos;apprenants</p>
        <Button variant="secondary" className="mt-4">Rejoindre</Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-primary">1,230</div>
            <div className="text-sm text-gray-600 mt-2">Membres</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-secondary">456</div>
            <div className="text-sm text-gray-600 mt-2">Posts</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-accent">89</div>
            <div className="text-sm text-gray-600 mt-2">Discussions</div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <div className="text-2xl font-bold text-primary">5</div>
            <div className="text-sm text-gray-600 mt-2">Événements</div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="pt-6">
          <h2 className="text-xl font-bold mb-4">À propos</h2>
          <p className="text-gray-600">Contenu de la communauté...</p>
        </CardContent>
      </Card>
    </div>
  );
}
