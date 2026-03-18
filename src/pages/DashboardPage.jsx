import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Play, 
  Users, 
  Radio, 
  Clock, 
  ChevronRight,
  TrendingUp,
  Calendar,
  Star
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { Button, Avatar, Badge, Card, CardContent } from '../components/ui'
import { formatDuration } from '../lib/utils'

// Donnees simulees
const continueWatching = [
  {
    id: 1,
    title: 'Les bases du Tajwid',
    chapter: 'Chapitre 3: Les Makharij',
    progress: 65,
    thumbnail: '/placeholder.svg?height=120&width=200',
    duration: 45
  },
  {
    id: 2,
    title: 'Comprendre le Fiqh',
    chapter: 'Chapitre 7: La priere',
    progress: 30,
    thumbnail: '/placeholder.svg?height=120&width=200',
    duration: 32
  }
]

const upcomingLives = [
  {
    id: 1,
    title: 'Session Q&A: Questions de Fiqh',
    instructor: 'Sheikh Ahmad Moussa',
    scheduledAt: new Date(Date.now() + 2 * 60 * 60 * 1000),
    attendees: 234
  },
  {
    id: 2,
    title: 'Lecture guidee: Sourate Al-Kahf',
    instructor: 'Ustadh Ibrahim Diallo',
    scheduledAt: new Date(Date.now() + 24 * 60 * 60 * 1000),
    attendees: 156
  }
]

const recommendedFormations = [
  {
    id: 1,
    title: 'Les 40 Hadiths de Nawawi',
    instructor: 'Sheikh Oumar Sy',
    thumbnail: '/placeholder.svg?height=200&width=300',
    rating: 4.9,
    students: 3210
  },
  {
    id: 2,
    title: 'Introduction a la Sira',
    instructor: 'Ustadha Fatima Ba',
    thumbnail: '/placeholder.svg?height=200&width=300',
    rating: 4.8,
    students: 1890
  },
  {
    id: 3,
    title: 'Les piliers de l\'Islam',
    instructor: 'Sheikh Mamadou Kane',
    thumbnail: '/placeholder.svg?height=200&width=300',
    rating: 4.9,
    students: 4521
  }
]

const recentReels = [
  { id: 1, thumbnail: '/placeholder.svg?height=300&width=200', views: 12500 },
  { id: 2, thumbnail: '/placeholder.svg?height=300&width=200', views: 8900 },
  { id: 3, thumbnail: '/placeholder.svg?height=300&width=200', views: 15600 },
  { id: 4, thumbnail: '/placeholder.svg?height=300&width=200', views: 7200 }
]

export default function DashboardPage() {
  const { user } = useAuth()

  const greeting = () => {
    const hour = new Date().getHours()
    if (hour < 12) return 'Bonjour'
    if (hour < 18) return 'Bon apres-midi'
    return 'Bonsoir'
  }

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-gradient-to-br from-primary to-emerald-600 rounded-2xl p-6 md:p-8 text-white relative overflow-hidden"
      >
        <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />
        
        <div className="relative z-10">
          <h1 className="text-2xl md:text-3xl font-serif font-bold mb-2">
            {greeting()}, {user?.firstName || 'Apprenant'} !
          </h1>
          <p className="text-emerald-100 mb-6">
            Continuez votre parcours d'apprentissage. Vous avez 2 cours en cours.
          </p>
          
          {/* Quick Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { icon: BookOpen, label: 'Formations', value: '3' },
              { icon: Clock, label: 'Heures', value: '12h' },
              { icon: Star, label: 'Certificats', value: '1' },
              { icon: TrendingUp, label: 'Progression', value: '65%' }
            ].map((stat, i) => (
              <div key={i} className="bg-white/10 backdrop-blur rounded-xl p-4">
                <stat.icon className="w-5 h-5 mb-2 text-emerald-200" />
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm text-emerald-200">{stat.label}</div>
              </div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Continue Watching */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-foreground">Continuer a apprendre</h2>
          <Link to="/my-formations" className="text-primary text-sm hover:underline flex items-center gap-1">
            Voir tout <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          {continueWatching.map((item) => (
            <Link 
              key={item.id} 
              to={`/formations/${item.id}/learn`}
              className="card-hover flex gap-4 p-4"
            >
              <div className="relative w-32 h-20 rounded-lg overflow-hidden flex-shrink-0">
                <img src={item.thumbnail} alt={item.title} className="w-full h-full object-cover" />
                <div className="absolute inset-0 flex items-center justify-center bg-black/30">
                  <Play className="w-8 h-8 text-white fill-white" />
                </div>
                {/* Progress bar */}
                <div className="absolute bottom-0 left-0 right-0 h-1 bg-black/30">
                  <div 
                    className="h-full bg-primary" 
                    style={{ width: `${item.progress}%` }} 
                  />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <h3 className="font-medium text-foreground truncate">{item.title}</h3>
                <p className="text-sm text-muted-foreground truncate">{item.chapter}</p>
                <div className="flex items-center gap-2 mt-2 text-sm text-muted-foreground">
                  <Clock className="w-4 h-4" />
                  <span>{formatDuration(item.duration)} restantes</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Two Column Layout */}
      <div className="grid lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-8">
          {/* Recommended Formations */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-foreground">Recommande pour vous</h2>
              <Link to="/formations" className="text-primary text-sm hover:underline flex items-center gap-1">
                Explorer <ChevronRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {recommendedFormations.map((formation) => (
                <Link key={formation.id} to={`/formations/${formation.id}`} className="card-hover">
                  <div className="relative h-36 overflow-hidden">
                    <img 
                      src={formation.thumbnail} 
                      alt={formation.title}
                      className="w-full h-full object-cover"
                    />
                  </div>
                  <div className="p-4">
                    <h3 className="font-medium text-foreground text-sm line-clamp-2 mb-2">
                      {formation.title}
                    </h3>
                    <p className="text-xs text-muted-foreground mb-2">{formation.instructor}</p>
                    <div className="flex items-center gap-2 text-xs text-muted-foreground">
                      <div className="flex items-center gap-1 text-gold-500">
                        <Star className="w-3 h-3 fill-current" />
                        {formation.rating}
                      </div>
                      <span>|</span>
                      <span>{formation.students} inscrits</span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>
          </section>

          {/* Reels */}
          <section>
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-foreground">Reels du moment</h2>
              <Link to="/reels" className="text-primary text-sm hover:underline flex items-center gap-1">
                Voir tout <ChevronRight className="w-4 h-4" />
              </Link>
            </div>

            <div className="grid grid-cols-4 gap-3">
              {recentReels.map((reel) => (
                <Link 
                  key={reel.id} 
                  to="/reels" 
                  className="relative aspect-[9/16] rounded-xl overflow-hidden group"
                >
                  <img 
                    src={reel.thumbnail} 
                    alt=""
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-2 left-2 text-white text-xs flex items-center gap-1">
                    <Play className="w-3 h-3" />
                    {(reel.views / 1000).toFixed(1)}K
                  </div>
                </Link>
              ))}
            </div>
          </section>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Upcoming Lives */}
          <Card>
            <CardContent className="p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-foreground flex items-center gap-2">
                  <Radio className="w-5 h-5 text-red-500" />
                  Lives a venir
                </h3>
                <Link to="/lives" className="text-primary text-sm hover:underline">
                  Voir tout
                </Link>
              </div>

              <div className="space-y-4">
                {upcomingLives.map((live) => (
                  <div key={live.id} className="flex gap-3">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0">
                      <Calendar className="w-5 h-5 text-primary" />
                    </div>
                    <div className="min-w-0">
                      <h4 className="font-medium text-foreground text-sm truncate">{live.title}</h4>
                      <p className="text-xs text-muted-foreground">{live.instructor}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="primary" size="sm">
                          {live.scheduledAt.toLocaleDateString('fr-FR', { 
                            day: 'numeric', 
                            month: 'short',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </Badge>
                        <span className="text-xs text-muted-foreground">
                          {live.attendees} inscrits
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              <Button variant="outline" className="w-full mt-4" size="sm">
                S'inscrire aux lives
              </Button>
            </CardContent>
          </Card>

          {/* Community Suggestion */}
          <Card>
            <CardContent className="p-5">
              <div className="flex items-center gap-2 mb-4">
                <Users className="w-5 h-5 text-primary" />
                <h3 className="font-semibold text-foreground">Communautes</h3>
              </div>

              <div className="bg-gradient-to-br from-primary/10 to-accent/10 rounded-xl p-4 text-center">
                <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-primary/20 flex items-center justify-center">
                  <Users className="w-8 h-8 text-primary" />
                </div>
                <h4 className="font-medium text-foreground mb-1">Groupe de lecture du Coran</h4>
                <p className="text-sm text-muted-foreground mb-4">
                  Rejoignez des sessions de lecture guidees chaque semaine
                </p>
                <Link to="/communities">
                  <Button size="sm" className="w-full">
                    Rejoindre une communaute
                  </Button>
                </Link>
              </div>
            </CardContent>
          </Card>

          {/* Daily Reminder */}
          <Card className="bg-gradient-to-br from-emerald-50 to-gold-50 border-primary/20">
            <CardContent className="p-5">
              <h3 className="font-semibold text-foreground mb-3">Rappel du jour</h3>
              <p className="font-arabic text-lg text-right leading-loose text-foreground mb-2">
                وَقُل رَّبِّ زِدْنِي عِلْمًا
              </p>
              <p className="text-sm text-muted-foreground italic">
                "Et dis: Seigneur, accroit mes connaissances"
              </p>
              <p className="text-xs text-primary mt-2">Sourate Ta-Ha, verset 114</p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
