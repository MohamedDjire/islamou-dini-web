import { forwardRef, useState } from 'react'
import { cn } from '../../lib/utils'
import { Eye, EyeOff, AlertCircle } from 'lucide-react'

const Input = forwardRef(
  (
    {
      className,
      type = 'text',
      label,
      error,
      helperText,
      leftIcon,
      rightIcon,
      disabled = false,
      required = false,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false)
    const isPassword = type === 'password'
    const inputType = isPassword ? (showPassword ? 'text' : 'password') : type

    return (
      <div className="w-full">
        {label && (
          <label className="label">
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}
        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground">
              {leftIcon}
            </div>
          )}
          <input
            ref={ref}
            type={inputType}
            className={cn(
              'w-full rounded-lg border bg-white px-4 py-2.5 text-foreground',
              'placeholder:text-muted-foreground',
              'focus:outline-none focus:ring-2 transition-all duration-200',
              error
                ? 'border-red-500 focus:border-red-500 focus:ring-red-500/20'
                : 'border-input focus:border-primary focus:ring-primary/20',
              leftIcon && 'pl-10',
              (rightIcon || isPassword) && 'pr-10',
              disabled && 'bg-muted cursor-not-allowed opacity-60',
              className
            )}
            disabled={disabled}
            {...props}
          />
          {isPassword && (
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
              tabIndex={-1}
            >
              {showPassword ? (
                <EyeOff className="h-5 w-5" />
              ) : (
                <Eye className="h-5 w-5" />
              )}
            </button>
          )}
          {rightIcon && !isPassword && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground">
              {rightIcon}
            </div>
          )}
        </div>
        {error && (
          <p className="mt-1.5 text-sm text-red-500 flex items-center gap-1">
            <AlertCircle className="h-4 w-4" />
            {error}
          </p>
        )}
        {helperText && !error && (
          <p className="mt-1.5 text-sm text-muted-foreground">{helperText}</p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

export default Input
