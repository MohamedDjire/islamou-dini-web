import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'react-hot-toast'
import { Mail, Lock } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { Button, Input } from '../../components/ui'

const loginSchema = z.object({
  email: z.string().email('Email invalide'),
  password: z.string().min(6, 'Le mot de passe doit contenir au moins 6 caracteres'),
})

export default function LoginPage() {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(loginSchema),
  })

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      const result = await login(data.email, data.password)
      if (result.success) {
        toast.success('Connexion reussie !')
        navigate('/dashboard')
      } else {
        toast.error(result.error || 'Erreur de connexion')
      }
    } catch (error) {
      toast.error('Une erreur est survenue')
    } finally {
      setIsLoading(false)
    }
  }

  // Demo login pour tester sans backend
  const handleDemoLogin = () => {
    // Simuler une connexion pour la demo
    localStorage.setItem('auth_token', 'demo_token')
    localStorage.setItem('refresh_token', 'demo_refresh')
    window.location.href = '/dashboard'
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-2xl font-serif font-bold text-foreground mb-2">
          Bon retour parmi nous
        </h1>
        <p className="text-muted-foreground">
          Connectez-vous pour continuer votre apprentissage
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
        <Input
          label="Email"
          type="email"
          placeholder="votre@email.com"
          leftIcon={<Mail className="h-5 w-5" />}
          error={errors.email?.message}
          {...register('email')}
        />

        <Input
          label="Mot de passe"
          type="password"
          placeholder="Votre mot de passe"
          leftIcon={<Lock className="h-5 w-5" />}
          error={errors.password?.message}
          {...register('password')}
        />

        <div className="flex items-center justify-between">
          <label className="flex items-center gap-2 cursor-pointer">
            <input 
              type="checkbox" 
              className="w-4 h-4 rounded border-input text-primary focus:ring-primary"
            />
            <span className="text-sm text-muted-foreground">Se souvenir de moi</span>
          </label>
          <Link 
            to="/forgot-password" 
            className="text-sm text-primary hover:text-emerald-800 font-medium"
          >
            Mot de passe oublie ?
          </Link>
        </div>

        <Button type="submit" className="w-full" size="lg" isLoading={isLoading}>
          Se connecter
        </Button>

        {/* Demo button */}
        <Button 
          type="button" 
          variant="outline" 
          className="w-full" 
          size="lg"
          onClick={handleDemoLogin}
        >
          Demo (sans backend)
        </Button>
      </form>

      {/* Divider */}
      <div className="divider-islamic my-8">
        <span className="text-muted-foreground text-sm px-4 bg-background">ou</span>
      </div>

      {/* Social Login */}
      <div className="space-y-3">
        <button className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg border border-border hover:bg-secondary transition-colors">
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          Continuer avec Google
        </button>

        <button className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg border border-border hover:bg-secondary transition-colors">
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
          </svg>
          Continuer avec Apple
        </button>
      </div>

      {/* Register link */}
      <p className="text-center mt-8 text-muted-foreground">
        Pas encore de compte ?{' '}
        <Link to="/register" className="text-primary hover:text-emerald-800 font-medium">
          Creer un compte
        </Link>
      </p>
    </div>
  )
}
