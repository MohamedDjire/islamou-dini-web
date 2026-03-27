import { useState } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, Users, Zap, Target } from 'lucide-react';
import { Button, Card, CardContent } from '../components/ui';

export default function HomePage() {
  const features = [
    {
      icon: BookOpen,
      title: 'Formations en Ligne',
      description: 'Accédez à des formations islamiques complètes et structurées',
    },
    {
      icon: Users,
      title: 'Communautés Actives',
      description: 'Connectez-vous avec d\'autres apprenants et partagez vos connaissances',
    },
    {
      icon: Zap,
      title: 'Contenu Moderne',
      description: 'Contenu vidéo, articles et discussions en temps réel',
    },
    {
      icon: Target,
      title: 'Votre Progression',
      description: 'Suivez votre progression et atteignez vos objectifs',
    },
  ];

  return (
    <div className="space-y-8 pb-8">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-secondary text-white py-12 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl font-bold mb-4">Bienvenue sur IslamouDini</h1>
          <p className="text-lg mb-8 opacity-90">
            Votre plateforme d'apprentissage islamique complète avec formations, communautés et partage de connaissances
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button variant="secondary" size="lg">
              <Link to="/formations">Explorer les Formations</Link>
            </Button>
            <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-primary">
              <Link to="/communities">Rejoindre une Communauté</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="max-w-4xl mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-900">Nos Fonctionnalités</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feature) => {
            const Icon = feature.icon;
            return (
              <Card key={feature.title}>
                <CardContent className="pt-6">
                  <div className="flex gap-4">
                    <div className="w-12 h-12 bg-primary bg-opacity-10 rounded-lg flex items-center justify-center flex-shrink-0">
                      <Icon className="text-primary" size={24} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
                      <p className="text-gray-600 text-sm">{feature.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </section>

      {/* Stats Section */}
      <section className="bg-gray-100 py-12 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-primary">500+</div>
              <div className="text-gray-600 text-sm mt-2">Formations</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-secondary">10k+</div>
              <div className="text-gray-600 text-sm mt-2">Utilisateurs</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-accent">50+</div>
              <div className="text-gray-600 text-sm mt-2">Communautés</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-primary">100%</div>
              <div className="text-gray-600 text-sm mt-2">Gratuit</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
