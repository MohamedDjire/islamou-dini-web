import { useState } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Star, Users } from 'lucide-react';
import { Card, CardContent, Button, Badge } from '../components/ui';

export default function CatalogPage() {
  const [formations] = useState([
    {
      id: 1,
      title: 'Introduction à l\'Islam',
      description: 'Les principes fondamentaux de l\'Islam expliqués de manière claire et progressive',
      image: '/placeholder.svg?height=200&width=300',
      instructor: 'Dr. Mohamed Ali',
      rating: 4.8,
      reviews: 324,
      students: 2500,
      level: 'Débutant',
      duration: '4 semaines',
      price: 'Gratuit',
    },
    {
      id: 2,
      title: 'Tafsir du Coran',
      description: 'Exégèse complète du Coran avec explications détaillées et approfondies',
      image: '/placeholder.svg?height=200&width=300',
      instructor: 'Dr. Fatima Al-Rashid',
      rating: 4.9,
      reviews: 456,
      students: 3200,
      level: 'Intermédiaire',
      duration: '12 semaines',
      price: 'Gratuit',
    },
    {
      id: 3,
      title: 'Fiqh Islamique',
      description: 'Jurisprudence islamique selon les quatre écoles de pensée',
      image: '/placeholder.svg?height=200&width=300',
      instructor: 'Cheikh Ahmed Hassan',
      rating: 4.7,
      reviews: 289,
      students: 1800,
      level: 'Avancé',
      duration: '16 semaines',
      price: 'Gratuit',
    },
  ]);

  return (
    <div className="max-w-6xl mx-auto p-4 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Catalogue de Formations</h1>
        <p className="text-gray-600">Découvrez nos formations islamiques complètes et structurées</p>
      </div>

      {/* Recherche et filtres */}
      <div className="flex gap-4 flex-wrap">
        <div className="flex-1 min-w-64 relative">
          <Search className="absolute left-3 top-3 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Chercher une formation..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <Button variant="outline" className="flex items-center gap-2">
          <Filter size={18} />
          Filtres
        </Button>
      </div>

      {/* Grille de formations */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {formations.map(formation => (
          <Link key={formation.id} to={`/formations/${formation.id}`}>
            <Card className="h-full hover:shadow-lg transition-shadow">
              <div className="relative overflow-hidden">
                <img
                  src={formation.image}
                  alt={formation.title}
                  className="w-full h-40 object-cover"
                />
                <Badge variant="primary" className="absolute top-3 left-3">
                  {formation.level}
                </Badge>
              </div>
              <CardContent className="pt-4">
                <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{formation.title}</h3>
                <p className="text-sm text-gray-600 mb-3 line-clamp-2">{formation.description}</p>

                <div className="space-y-3 text-sm">
                  <div className="flex items-center justify-between text-gray-600">
                    <span>{formation.instructor}</span>
                  </div>

                  <div className="flex items-center gap-2">
                    <Star className="text-yellow-400" size={16} fill="currentColor" />
                    <span className="font-semibold text-gray-900">{formation.rating}</span>
                    <span className="text-gray-500">({formation.reviews})</span>
                  </div>

                  <div className="flex items-center gap-2 text-gray-600">
                    <Users size={16} />
                    <span>{formation.students} étudiants</span>
                  </div>

                  <div className="flex justify-between items-center pt-3 border-t border-gray-200">
                    <span className="text-xs text-gray-500">{formation.duration}</span>
                    <span className="font-bold text-primary">{formation.price}</span>
                  </div>
                </div>

                <Button variant="secondary" className="w-full mt-4">
                  S&apos;inscrire
                </Button>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
}
