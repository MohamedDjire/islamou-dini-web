import { forwardRef } from 'react'
import { cn } from '../../lib/utils'
import { Loader2 } from 'lucide-react'

const variants = {
  primary: 'bg-primary text-primary-foreground hover:bg-emerald-800 focus:ring-primary',
  secondary: 'bg-secondary text-secondary-foreground hover:bg-cream-300 focus:ring-secondary',
  outline: 'border-2 border-primary text-primary bg-transparent hover:bg-primary hover:text-primary-foreground focus:ring-primary',
  ghost: 'bg-transparent text-foreground hover:bg-secondary focus:ring-secondary',
  accent: 'bg-accent text-accent-foreground hover:bg-gold-600 focus:ring-accent',
  danger: 'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500',
  link: 'bg-transparent text-primary underline-offset-4 hover:underline p-0 h-auto',
}

const sizes = {
  sm: 'px-3 py-1.5 text-sm rounded-md',
  md: 'px-4 py-2 text-base rounded-lg',
  lg: 'px-6 py-3 text-lg rounded-lg',
  xl: 'px-8 py-4 text-xl rounded-xl',
  icon: 'p-2 rounded-lg',
}

const Button = forwardRef(
  (
    {
      className,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      disabled = false,
      leftIcon,
      rightIcon,
      children,
      ...props
    },
    ref
  ) => {
    return (
      <button
        ref={ref}
        className={cn(
          'inline-flex items-center justify-center gap-2 font-medium transition-all duration-200',
          'focus:outline-none focus:ring-2 focus:ring-offset-2',
          'disabled:opacity-50 disabled:pointer-events-none',
          variants[variant],
          sizes[size],
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <Loader2 className="h-4 w-4 animate-spin" />
        ) : leftIcon ? (
          <span className="flex-shrink-0">{leftIcon}</span>
        ) : null}
        {children}
        {rightIcon && !isLoading && (
          <span className="flex-shrink-0">{rightIcon}</span>
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'

export default Button
