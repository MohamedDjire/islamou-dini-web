import { useParams } from 'react-router-dom';
import { Play, BookOpen, Clock, Users } from 'lucide-react';
import { Card, CardContent, Button } from '../components/ui';

export default function FormationDetailPage() {
  const { id } = useParams();

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <div className="bg-gradient-to-r from-primary to-secondary text-white h-64 rounded-lg flex items-center justify-center">
        <Play size={64} fill="white" />
      </div>

      <div className="space-y-4">
        <h1 className="text-3xl font-bold text-gray-900">Formation #{id}</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="flex items-center gap-2 text-gray-600">
            <Clock size={20} />
            12 semaines
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <BookOpen size={20} />
            24 leçons
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <Users size={20} />
            2500 étudiants
          </div>
        </div>

        <Button size="lg">S&apos;inscrire</Button>
      </div>

      <Card>
        <CardContent className="pt-6">
          <h2 className="text-xl font-bold mb-4">À propos</h2>
          <p className="text-gray-600">Contenu détaillé de la formation...</p>
        </CardContent>
      </Card>
    </div>
  );
}
