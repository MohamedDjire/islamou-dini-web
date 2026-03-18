import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  BookOpen, 
  Play, 
  Users, 
  Radio, 
  Star, 
  ChevronRight,
  CheckCircle,
  ArrowRight,
  Quote
} from 'lucide-react'
import { Button, Avatar, Badge } from '../components/ui'

// Animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
}

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
}

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-background/80 backdrop-blur-md border-b border-border/50">
        <div className="container-app">
          <div className="flex items-center justify-between h-16">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-9 h-9 rounded-lg bg-gradient-emerald flex items-center justify-center">
                <span className="text-white font-serif font-bold text-lg">I</span>
              </div>
              <span className="font-serif font-semibold text-xl text-foreground">
                Islamou<span className="text-primary">Dini</span>
              </span>
            </Link>

            <nav className="hidden md:flex items-center gap-8">
              <a href="#features" className="text-muted-foreground hover:text-foreground transition-colors">
                Fonctionnalites
              </a>
              <a href="#formations" className="text-muted-foreground hover:text-foreground transition-colors">
                Formations
              </a>
              <a href="#testimonials" className="text-muted-foreground hover:text-foreground transition-colors">
                Temoignages
              </a>
              <a href="#pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                Tarifs
              </a>
            </nav>

            <div className="flex items-center gap-3">
              <Link to="/login">
                <Button variant="ghost" size="sm">Connexion</Button>
              </Link>
              <Link to="/register">
                <Button size="sm">Commencer gratuitement</Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative pt-32 pb-20 md:pt-40 md:pb-32 overflow-hidden islamic-pattern-bg">
        {/* Decorative elements */}
        <div className="absolute top-20 right-0 w-96 h-96 bg-primary/5 rounded-full blur-3xl" />
        <div className="absolute bottom-0 left-0 w-80 h-80 bg-accent/5 rounded-full blur-3xl" />

        <div className="container-app relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <motion.div {...fadeInUp}>
              <Badge variant="accent" size="lg" className="mb-6">
                <Star className="w-4 h-4 mr-1" />
                Plus de 10 000 apprenants nous font confiance
              </Badge>
            </motion.div>

            <motion.h1 
              className="font-serif text-4xl md:text-5xl lg:text-6xl font-bold text-foreground mb-6 leading-tight text-balance"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.1 }}
            >
              Apprendre l'Islam{' '}
              <span className="text-primary">n'a jamais ete</span>{' '}
              aussi accessible
            </motion.h1>

            <motion.p 
              className="text-lg md:text-xl text-muted-foreground mb-8 max-w-2xl mx-auto leading-relaxed"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              Formations video de qualite, reels inspirants, communautes de lecture du Coran 
              et lives diriges par des savants reconnus. Tout ce dont vous avez besoin pour 
              approfondir votre foi.
            </motion.p>

            <motion.div 
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
            >
              <Link to="/register">
                <Button size="lg" rightIcon={<ArrowRight className="w-5 h-5" />}>
                  Commencer gratuitement
                </Button>
              </Link>
              <Link to="/formations">
                <Button variant="outline" size="lg">
                  Decouvrir les formations
                </Button>
              </Link>
            </motion.div>

            {/* Stats */}
            <motion.div 
              className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 pt-12 border-t border-border"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.5 }}
            >
              {[
                { value: '100+', label: 'Formations' },
                { value: '50+', label: 'Formateurs' },
                { value: '10K+', label: 'Apprenants' },
                { value: '4.9/5', label: 'Satisfaction' },
              ].map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl md:text-4xl font-bold text-primary mb-1">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="section bg-card">
        <div className="container-app">
          <div className="text-center mb-16">
            <Badge variant="primary" className="mb-4">Fonctionnalites</Badge>
            <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">
              Une plateforme complete pour votre parcours spirituel
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Decouvrez tous les outils dont vous avez besoin pour apprendre, pratiquer et partager
            </p>
          </div>

          <motion.div 
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-6"
            variants={staggerContainer}
            initial="initial"
            whileInView="animate"
            viewport={{ once: true }}
          >
            {[
              {
                icon: BookOpen,
                title: 'Formations Video',
                description: 'Cours structures par des experts reconnus, du niveau debutant a avance.',
                color: 'bg-primary/10 text-primary'
              },
              {
                icon: Play,
                title: 'Reels Inspirants',
                description: 'Courtes videos pour apprendre et se rappeler au quotidien.',
                color: 'bg-accent/20 text-gold-700'
              },
              {
                icon: Users,
                title: 'Communautes de Lecture',
                description: 'Rejoignez des groupes pour lire et memoriser le Coran ensemble.',
                color: 'bg-emerald-100 text-emerald-700'
              },
              {
                icon: Radio,
                title: 'Lives Diriges',
                description: 'Sessions interactives en direct avec vos formateurs preferes.',
                color: 'bg-blue-100 text-blue-700'
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                variants={fadeInUp}
                className="bg-background rounded-2xl p-6 border border-border/50 hover:border-primary/30 hover:shadow-elevated transition-all duration-300"
              >
                <div className={`w-14 h-14 rounded-xl ${feature.color} flex items-center justify-center mb-4`}>
                  <feature.icon className="w-7 h-7" />
                </div>
                <h3 className="font-semibold text-lg text-foreground mb-2">{feature.title}</h3>
                <p className="text-muted-foreground text-sm leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Formations Preview Section */}
      <section id="formations" className="section">
        <div className="container-app">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-12">
            <div>
              <Badge variant="primary" className="mb-4">Formations populaires</Badge>
              <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground text-balance">
                Des cours pour tous les niveaux
              </h2>
            </div>
            <Link to="/formations" className="text-primary hover:text-emerald-800 font-medium flex items-center gap-1 group">
              Voir toutes les formations
              <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[
              {
                title: 'Les bases du Tajwid',
                instructor: 'Sheikh Ahmad Moussa',
                image: '/placeholder.svg?height=200&width=400',
                category: 'Coran',
                level: 'Debutant',
                duration: '12h',
                students: 2340,
                rating: 4.9
              },
              {
                title: 'Comprendre le Fiqh Malikite',
                instructor: 'Ustadh Ibrahim Diallo',
                image: '/placeholder.svg?height=200&width=400',
                category: 'Fiqh',
                level: 'Intermediaire',
                duration: '20h',
                students: 1856,
                rating: 4.8
              },
              {
                title: 'Les 40 Hadiths de Nawawi',
                instructor: 'Sheikh Oumar Sy',
                image: '/placeholder.svg?height=200&width=400',
                category: 'Hadith',
                level: 'Tous niveaux',
                duration: '8h',
                students: 3210,
                rating: 4.9
              }
            ].map((formation, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="card-hover group"
              >
                <div className="relative h-48 overflow-hidden">
                  <img 
                    src={formation.image} 
                    alt={formation.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
                  <div className="absolute bottom-4 left-4 right-4">
                    <Badge variant="accent" size="sm">{formation.category}</Badge>
                  </div>
                </div>
                <div className="p-5">
                  <h3 className="font-semibold text-foreground mb-2 group-hover:text-primary transition-colors">
                    {formation.title}
                  </h3>
                  <div className="flex items-center gap-2 mb-3">
                    <Avatar name={formation.instructor} size="xs" />
                    <span className="text-sm text-muted-foreground">{formation.instructor}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center gap-3 text-muted-foreground">
                      <span>{formation.duration}</span>
                      <span>{formation.students} inscrits</span>
                    </div>
                    <div className="flex items-center gap-1 text-gold-500">
                      <Star className="w-4 h-4 fill-current" />
                      <span className="font-medium">{formation.rating}</span>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section id="testimonials" className="section bg-gradient-to-br from-emerald-800 via-emerald-700 to-emerald-900 text-white relative overflow-hidden">
        {/* Pattern overlay */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0 islamic-pattern-bg" />
        </div>

        <div className="container-app relative z-10">
          <div className="text-center mb-16">
            <Badge className="bg-white/20 text-white border-white/30 mb-4">Temoignages</Badge>
            <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4 text-balance">
              Ce que disent nos apprenants
            </h2>
            <p className="text-emerald-100 max-w-2xl mx-auto">
              Des milliers de musulmans nous font confiance pour leur parcours d'apprentissage
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                name: 'Fatima Diop',
                role: 'Etudiante',
                content: "Grace a IslamouDini, j'ai pu apprendre le Tajwid depuis chez moi. Les formateurs sont excellents et la plateforme est tres intuitive.",
                avatar: '/placeholder.svg?height=60&width=60'
              },
              {
                name: 'Moussa Traore',
                role: 'Entrepreneur',
                content: "Les reels quotidiens me permettent de rester connecte a ma foi malgre mon emploi du temps charge. Un excellent investissement.",
                avatar: '/placeholder.svg?height=60&width=60'
              },
              {
                name: 'Aisha Coulibaly',
                role: 'Enseignante',
                content: "La communaute de lecture du Coran m'a aidee a rester motivee. J'ai progresse plus en 3 mois qu'en 2 ans seule.",
                avatar: '/placeholder.svg?height=60&width=60'
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/10 backdrop-blur rounded-2xl p-6 border border-white/20"
              >
                <Quote className="w-8 h-8 text-gold-400 mb-4" />
                <p className="text-emerald-50 mb-6 leading-relaxed">{testimonial.content}</p>
                <div className="flex items-center gap-3">
                  <Avatar src={testimonial.avatar} name={testimonial.name} size="md" />
                  <div>
                    <div className="font-medium">{testimonial.name}</div>
                    <div className="text-sm text-emerald-200">{testimonial.role}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="section">
        <div className="container-app">
          <div className="text-center mb-16">
            <Badge variant="primary" className="mb-4">Tarifs</Badge>
            <h2 className="font-serif text-3xl md:text-4xl font-bold text-foreground mb-4 text-balance">
              Choisissez votre formule
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Commencez gratuitement et passez Premium pour debloquer toutes les fonctionnalites
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-5xl mx-auto">
            {/* Free Plan */}
            <div className="card p-8">
              <h3 className="font-semibold text-xl text-foreground mb-2">Gratuit</h3>
              <p className="text-muted-foreground text-sm mb-6">Pour decouvrir la plateforme</p>
              <div className="mb-6">
                <span className="text-4xl font-bold text-foreground">0 FCFA</span>
                <span className="text-muted-foreground">/mois</span>
              </div>
              <ul className="space-y-3 mb-8">
                {[
                  'Acces aux formations gratuites',
                  'Reels illimites',
                  '1 communaute de lecture',
                  'Acces aux lives publics'
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <Link to="/register" className="block">
                <Button variant="outline" className="w-full">Commencer</Button>
              </Link>
            </div>

            {/* Premium Plan */}
            <div className="card p-8 border-2 border-primary relative">
              <div className="absolute -top-3 left-1/2 -translate-x-1/2">
                <Badge variant="primary">Populaire</Badge>
              </div>
              <h3 className="font-semibold text-xl text-foreground mb-2">Premium</h3>
              <p className="text-muted-foreground text-sm mb-6">Pour un apprentissage complet</p>
              <div className="mb-6">
                <span className="text-4xl font-bold text-foreground">5 000 FCFA</span>
                <span className="text-muted-foreground">/mois</span>
              </div>
              <ul className="space-y-3 mb-8">
                {[
                  'Toutes les formations',
                  'Telechargement hors-ligne',
                  'Communautes illimitees',
                  'Lives exclusifs + replays',
                  'Certificats de completion',
                  'Support prioritaire'
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-foreground">
                    <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <Link to="/register?plan=premium" className="block">
                <Button className="w-full">Passer Premium</Button>
              </Link>
            </div>

            {/* Institution Plan */}
            <div className="card p-8">
              <h3 className="font-semibold text-xl text-foreground mb-2">Institution</h3>
              <p className="text-muted-foreground text-sm mb-6">Pour les ecoles et mosquees</p>
              <div className="mb-6">
                <span className="text-4xl font-bold text-foreground">Sur devis</span>
              </div>
              <ul className="space-y-3 mb-8">
                {[
                  'Tout Premium inclus',
                  'Comptes multi-utilisateurs',
                  'Tableau de bord admin',
                  'Formations personnalisees',
                  'Integration API',
                  'Account manager dedie'
                ].map((feature, i) => (
                  <li key={i} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <CheckCircle className="w-5 h-5 text-primary flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
              <a href="mailto:contact@islamoudini.com">
                <Button variant="outline" className="w-full">Nous contacter</Button>
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section bg-card">
        <div className="container-app">
          <div className="bg-gradient-to-br from-primary to-emerald-600 rounded-3xl p-8 md:p-12 text-center text-white relative overflow-hidden">
            {/* Decorative */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-48 h-48 bg-white/10 rounded-full blur-3xl" />

            <div className="relative z-10 max-w-2xl mx-auto">
              <h2 className="font-serif text-3xl md:text-4xl font-bold mb-4 text-balance">
                Pret a commencer votre parcours ?
              </h2>
              <p className="text-emerald-100 mb-8">
                Rejoignez des milliers de musulmans qui apprennent et grandissent spirituellement chaque jour.
              </p>
              <Link to="/register">
                <Button 
                  size="lg" 
                  className="bg-white text-primary hover:bg-cream-100"
                  rightIcon={<ArrowRight className="w-5 h-5" />}
                >
                  Creer un compte gratuit
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-foreground text-cream-100 py-12">
        <div className="container-app">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-9 h-9 rounded-lg bg-primary flex items-center justify-center">
                  <span className="text-white font-serif font-bold text-lg">I</span>
                </div>
                <span className="font-serif font-semibold text-xl text-white">
                  Islamou<span className="text-gold-400">Dini</span>
                </span>
              </div>
              <p className="text-cream-300 text-sm">
                Votre plateforme d'education islamique en ligne. Apprenez, pratiquez, partagez.
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Plateforme</h4>
              <ul className="space-y-2 text-sm text-cream-300">
                <li><Link to="/formations" className="hover:text-white transition-colors">Formations</Link></li>
                <li><Link to="/reels" className="hover:text-white transition-colors">Reels</Link></li>
                <li><Link to="/communities" className="hover:text-white transition-colors">Communautes</Link></li>
                <li><Link to="/lives" className="hover:text-white transition-colors">Lives</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Entreprise</h4>
              <ul className="space-y-2 text-sm text-cream-300">
                <li><a href="#" className="hover:text-white transition-colors">A propos</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Devenir formateur</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Carrieres</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Contact</a></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-cream-300">
                <li><a href="#" className="hover:text-white transition-colors">Conditions d'utilisation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Politique de confidentialite</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Mentions legales</a></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-cream-800 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-cream-400">
            <p>&copy; {new Date().getFullYear()} IslamouDini. Tous droits reserves.</p>
            <p className="font-arabic text-base">بسم الله الرحمن الرحيم</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
