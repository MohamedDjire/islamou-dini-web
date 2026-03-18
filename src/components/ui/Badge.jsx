import { cn } from '../../lib/utils'

const variants = {
  primary: 'bg-primary/10 text-primary',
  secondary: 'bg-secondary text-secondary-foreground',
  accent: 'bg-accent/20 text-gold-700',
  success: 'bg-green-100 text-green-700',
  warning: 'bg-amber-100 text-amber-700',
  error: 'bg-red-100 text-red-700',
  info: 'bg-blue-100 text-blue-700',
  outline: 'border border-current bg-transparent',
}

const sizes = {
  sm: 'px-2 py-0.5 text-xs',
  md: 'px-2.5 py-0.5 text-sm',
  lg: 'px-3 py-1 text-sm',
}

export default function Badge({
  variant = 'primary',
  size = 'md',
  className,
  children,
  icon,
  ...props
}) {
  return (
    <span
      className={cn(
        'inline-flex items-center gap-1 rounded-full font-medium',
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    >
      {icon && <span className="flex-shrink-0">{icon}</span>}
      {children}
    </span>
  )
}
