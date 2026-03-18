import { cn } from '../../lib/utils'

const sizes = {
  sm: 'w-4 h-4 border-2',
  md: 'w-8 h-8 border-2',
  lg: 'w-12 h-12 border-3',
  xl: 'w-16 h-16 border-4',
}

export default function Loader({ size = 'md', className, fullScreen = false }) {
  const spinner = (
    <div
      className={cn(
        'rounded-full border-primary/30 border-t-primary animate-spin',
        sizes[size],
        className
      )}
    />
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm z-50">
        <div className="flex flex-col items-center gap-4">
          {spinner}
          <p className="text-muted-foreground animate-pulse">Chargement...</p>
        </div>
      </div>
    )
  }

  return spinner
}

export function PageLoader() {
  return (
    <div className="min-h-[400px] flex items-center justify-center">
      <Loader size="lg" />
    </div>
  )
}

export function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn('bg-muted animate-pulse rounded', className)}
      {...props}
    />
  )
}

export function CardSkeleton() {
  return (
    <div className="bg-card rounded-xl border border-border/50 overflow-hidden">
      <Skeleton className="h-48 w-full rounded-none" />
      <div className="p-5 space-y-3">
        <Skeleton className="h-4 w-3/4" />
        <Skeleton className="h-3 w-full" />
        <Skeleton className="h-3 w-2/3" />
        <div className="flex items-center gap-2 pt-2">
          <Skeleton className="h-8 w-8 rounded-full" />
          <Skeleton className="h-3 w-24" />
        </div>
      </div>
    </div>
  )
}

export function ListSkeleton({ count = 5 }) {
  return (
    <div className="space-y-4">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="flex items-center gap-4">
          <Skeleton className="h-12 w-12 rounded-full" />
          <div className="flex-1 space-y-2">
            <Skeleton className="h-4 w-1/3" />
            <Skeleton className="h-3 w-2/3" />
          </div>
        </div>
      ))}
    </div>
  )
}
