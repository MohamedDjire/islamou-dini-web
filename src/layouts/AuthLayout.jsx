import { Link, Outlet } from 'react-router-dom'

export default function AuthLayout() {
  return (
    <div className="min-h-screen bg-background islamic-pattern-bg flex">
      {/* Left side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-emerald-800 via-emerald-700 to-emerald-900 relative overflow-hidden">
        {/* Pattern overlay */}
        <div className="absolute inset-0 opacity-10">
          <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
            <pattern id="islamic-pattern-auth" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
              <path d="M10 0L20 10L10 20L0 10Z" fill="currentColor" className="text-white"/>
            </pattern>
            <rect width="100" height="100" fill="url(#islamic-pattern-auth)"/>
          </svg>
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center p-12 text-white">
          <Link to="/" className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur flex items-center justify-center">
              <span className="text-white font-serif font-bold text-2xl">I</span>
            </div>
            <span className="font-serif font-semibold text-3xl">
              Islamou<span className="text-gold-400">Dini</span>
            </span>
          </Link>

          <h1 className="font-serif text-4xl font-bold mb-4 leading-tight text-balance">
            Apprendre l'Islam n'a jamais ete aussi accessible
          </h1>
          
          <p className="text-emerald-100 text-lg mb-8 leading-relaxed">
            Rejoignez notre communaute et accedez a des formations de qualite, 
            des reels inspirants et des sessions de lecture du Coran guidees.
          </p>

          {/* Features */}
          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                </svg>
              </div>
              <span>Formations video par des experts</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                </svg>
              </div>
              <span>Communautes de lecture du Coran</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                </svg>
              </div>
              <span>Lives et sessions interactives</span>
            </div>
          </div>

          {/* Quote */}
          <div className="mt-12 p-6 bg-white/10 backdrop-blur rounded-xl border border-white/20">
            <p className="font-arabic text-xl text-right mb-3 leading-loose">
              طَلَبُ الْعِلْمِ فَرِيضَةٌ عَلَى كُلِّ مُسْلِمٍ
            </p>
            <p className="text-emerald-100 text-sm italic">
              "La recherche du savoir est une obligation pour tout musulman"
            </p>
            <p className="text-emerald-200 text-xs mt-1">- Hadith (Ibn Majah)</p>
          </div>
        </div>
      </div>

      {/* Right side - Form */}
      <div className="flex-1 flex items-center justify-center p-6 lg:p-12">
        <div className="w-full max-w-md">
          {/* Mobile logo */}
          <div className="lg:hidden text-center mb-8">
            <Link to="/" className="inline-flex items-center gap-2">
              <div className="w-10 h-10 rounded-lg bg-gradient-emerald flex items-center justify-center">
                <span className="text-white font-serif font-bold text-xl">I</span>
              </div>
              <span className="font-serif font-semibold text-2xl text-foreground">
                Islamou<span className="text-primary">Dini</span>
              </span>
            </Link>
          </div>

          <Outlet />
        </div>
      </div>
    </div>
  )
}
