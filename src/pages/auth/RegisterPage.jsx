import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { toast } from 'react-hot-toast'
import { User, Mail, Lock, Phone } from 'lucide-react'
import { useAuth } from '../../context/AuthContext'
import { Button, Input } from '../../components/ui'

const registerSchema = z.object({
  firstName: z.string().min(2, 'Le prenom doit contenir au moins 2 caracteres'),
  lastName: z.string().min(2, 'Le nom doit contenir au moins 2 caracteres'),
  email: z.string().email('Email invalide'),
  phone: z.string().optional(),
  password: z.string().min(8, 'Le mot de passe doit contenir au moins 8 caracteres'),
  confirmPassword: z.string(),
  acceptTerms: z.boolean().refine((val) => val === true, {
    message: 'Vous devez accepter les conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Les mots de passe ne correspondent pas',
  path: ['confirmPassword'],
})

export default function RegisterPage() {
  const navigate = useNavigate()
  const { register: registerUser } = useAuth()
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(registerSchema),
  })

  const onSubmit = async (data) => {
    setIsLoading(true)
    try {
      const result = await registerUser({
        firstName: data.firstName,
        lastName: data.lastName,
        email: data.email,
        phone: data.phone,
        password: data.password,
      })

      if (result.success) {
        toast.success('Compte cree avec succes !')
        navigate('/dashboard')
      } else {
        toast.error(result.error || "Erreur lors de l'inscription")
      }
    } catch (error) {
      toast.error('Une erreur est survenue')
    } finally {
      setIsLoading(false)
    }
  }

  // Demo register pour tester sans backend
  const handleDemoRegister = () => {
    localStorage.setItem('auth_token', 'demo_token')
    localStorage.setItem('refresh_token', 'demo_refresh')
    window.location.href = '/dashboard'
  }

  return (
    <div>
      <div className="text-center mb-8">
        <h1 className="text-2xl font-serif font-bold text-foreground mb-2">
          Creer votre compte
        </h1>
        <p className="text-muted-foreground">
          Rejoignez des milliers d'apprenants
        </p>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <Input
            label="Prenom"
            placeholder="Votre prenom"
            leftIcon={<User className="h-5 w-5" />}
            error={errors.firstName?.message}
            {...register('firstName')}
          />

          <Input
            label="Nom"
            placeholder="Votre nom"
            error={errors.lastName?.message}
            {...register('lastName')}
          />
        </div>

        <Input
          label="Email"
          type="email"
          placeholder="votre@email.com"
          leftIcon={<Mail className="h-5 w-5" />}
          error={errors.email?.message}
          {...register('email')}
        />

        <Input
          label="Telephone (optionnel)"
          type="tel"
          placeholder="+221 77 000 00 00"
          leftIcon={<Phone className="h-5 w-5" />}
          error={errors.phone?.message}
          {...register('phone')}
        />

        <Input
          label="Mot de passe"
          type="password"
          placeholder="Au moins 8 caracteres"
          leftIcon={<Lock className="h-5 w-5" />}
          error={errors.password?.message}
          {...register('password')}
        />

        <Input
          label="Confirmer le mot de passe"
          type="password"
          placeholder="Confirmer votre mot de passe"
          leftIcon={<Lock className="h-5 w-5" />}
          error={errors.confirmPassword?.message}
          {...register('confirmPassword')}
        />

        <label className="flex items-start gap-3 cursor-pointer">
          <input 
            type="checkbox" 
            className="w-4 h-4 mt-0.5 rounded border-input text-primary focus:ring-primary"
            {...register('acceptTerms')}
          />
          <span className="text-sm text-muted-foreground">
            J'accepte les{' '}
            <a href="#" className="text-primary hover:underline">conditions d'utilisation</a>
            {' '}et la{' '}
            <a href="#" className="text-primary hover:underline">politique de confidentialite</a>
          </span>
        </label>
        {errors.acceptTerms && (
          <p className="text-sm text-red-500">{errors.acceptTerms.message}</p>
        )}

        <Button type="submit" className="w-full" size="lg" isLoading={isLoading}>
          Creer mon compte
        </Button>

        {/* Demo button */}
        <Button 
          type="button" 
          variant="outline" 
          className="w-full" 
          size="lg"
          onClick={handleDemoRegister}
        >
          Demo (sans backend)
        </Button>
      </form>

      {/* Divider */}
      <div className="divider-islamic my-6">
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
          S'inscrire avec Google
        </button>

        <button className="w-full flex items-center justify-center gap-3 px-4 py-3 rounded-lg border border-border hover:bg-secondary transition-colors">
          <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
            <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
          </svg>
          S'inscrire avec Apple
        </button>
      </div>

      {/* Login link */}
      <p className="text-center mt-8 text-muted-foreground">
        Deja un compte ?{' '}
        <Link to="/login" className="text-primary hover:text-emerald-800 font-medium">
          Se connecter
        </Link>
      </p>
    </div>
  )
}
