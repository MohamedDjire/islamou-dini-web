import { cn, getInitials } from '../../lib/utils'

const sizes = {
  xs: 'w-6 h-6 text-xs',
  sm: 'w-8 h-8 text-xs',
  md: 'w-10 h-10 text-sm',
  lg: 'w-14 h-14 text-base',
  xl: 'w-20 h-20 text-xl',
  '2xl': 'w-28 h-28 text-2xl',
}

export default function Avatar({
  src,
  alt,
  name,
  size = 'md',
  className,
  online = false,
  ...props
}) {
  const initials = getInitials(name || alt)

  return (
    <div className={cn('relative inline-block', className)} {...props}>
      {src ? (
        <img
          src={src}
          alt={alt || name || 'Avatar'}
          className={cn(
            'rounded-full object-cover bg-muted',
            sizes[size]
          )}
        />
      ) : (
        <div
          className={cn(
            'rounded-full flex items-center justify-center font-medium',
            'bg-gradient-emerald text-white',
            sizes[size]
          )}
        >
          {initials}
        </div>
      )}
      {online && (
        <span
          className={cn(
            'absolute bottom-0 right-0 block rounded-full bg-green-500 ring-2 ring-white',
            size === 'xs' && 'w-1.5 h-1.5',
            size === 'sm' && 'w-2 h-2',
            size === 'md' && 'w-2.5 h-2.5',
            (size === 'lg' || size === 'xl' || size === '2xl') && 'w-3 h-3'
          )}
        />
      )}
    </div>
  )
}

export function AvatarGroup({ avatars, max = 4, size = 'md', className }) {
  const displayAvatars = avatars.slice(0, max)
  const remaining = avatars.length - max

  return (
    <div className={cn('flex -space-x-2', className)}>
      {displayAvatars.map((avatar, index) => (
        <Avatar
          key={index}
          src={avatar.src}
          name={avatar.name}
          size={size}
          className="ring-2 ring-white"
        />
      ))}
      {remaining > 0 && (
        <div
          className={cn(
            'rounded-full flex items-center justify-center font-medium',
            'bg-muted text-muted-foreground ring-2 ring-white',
            sizes[size]
          )}
        >
          +{remaining}
        </div>
      )}
    </div>
  )
}
