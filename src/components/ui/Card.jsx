import { cn } from '../../lib/utils'

export function Card({ className, hover = false, children, ...props }) {
  return (
    <div
      className={cn(
        'bg-card rounded-xl border border-border/50 shadow-soft overflow-hidden',
        hover && 'transition-all duration-300 hover:shadow-elevated hover:-translate-y-1',
        className
      )}
      {...props}
    >
      {children}
    </div>
  )
}

export function CardHeader({ className, children, ...props }) {
  return (
    <div className={cn('p-5 pb-0', className)} {...props}>
      {children}
    </div>
  )
}

export function CardTitle({ className, children, ...props }) {
  return (
    <h3 className={cn('text-lg font-semibold text-foreground', className)} {...props}>
      {children}
    </h3>
  )
}

export function CardDescription({ className, children, ...props }) {
  return (
    <p className={cn('text-sm text-muted-foreground mt-1', className)} {...props}>
      {children}
    </p>
  )
}

export function CardContent({ className, children, ...props }) {
  return (
    <div className={cn('p-5', className)} {...props}>
      {children}
    </div>
  )
}

export function CardFooter({ className, children, ...props }) {
  return (
    <div className={cn('p-5 pt-0 flex items-center', className)} {...props}>
      {children}
    </div>
  )
}

export function CardImage({ src, alt, className, overlay = false, ...props }) {
  return (
    <div className={cn('relative overflow-hidden', className)}>
      <img
        src={src}
        alt={alt}
        className="w-full h-full object-cover"
        {...props}
      />
      {overlay && (
        <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
      )}
    </div>
  )
}

export default Card
