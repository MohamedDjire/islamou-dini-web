import { useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import { cn } from '../../lib/utils'
import { X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const sizes = {
  sm: 'max-w-md',
  md: 'max-w-lg',
  lg: 'max-w-2xl',
  xl: 'max-w-4xl',
  full: 'max-w-full mx-4',
}

export default function Modal({
  isOpen,
  onClose,
  title,
  description,
  size = 'md',
  showClose = true,
  closeOnOverlay = true,
  className,
  children,
}) {
  const modalRef = useRef(null)

  // Fermer avec Escape
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') onClose()
    }

    if (isOpen) {
      document.addEventListener('keydown', handleEscape)
      document.body.style.overflow = 'hidden'
    }

    return () => {
      document.removeEventListener('keydown', handleEscape)
      document.body.style.overflow = 'unset'
    }
  }, [isOpen, onClose])

  // Focus trap
  useEffect(() => {
    if (isOpen && modalRef.current) {
      modalRef.current.focus()
    }
  }, [isOpen])

  if (typeof window === 'undefined') return null

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={closeOnOverlay ? onClose : undefined}
            aria-hidden="true"
          />

          {/* Modal */}
          <motion.div
            ref={modalRef}
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2 }}
            className={cn(
              'relative w-full bg-card rounded-xl shadow-elevated z-10',
              sizes[size],
              className
            )}
            role="dialog"
            aria-modal="true"
            aria-labelledby={title ? 'modal-title' : undefined}
            aria-describedby={description ? 'modal-description' : undefined}
            tabIndex={-1}
          >
            {/* Header */}
            {(title || showClose) && (
              <div className="flex items-start justify-between p-5 border-b border-border">
                <div>
                  {title && (
                    <h2 id="modal-title" className="text-lg font-semibold text-foreground">
                      {title}
                    </h2>
                  )}
                  {description && (
                    <p id="modal-description" className="text-sm text-muted-foreground mt-1">
                      {description}
                    </p>
                  )}
                </div>
                {showClose && (
                  <button
                    onClick={onClose}
                    className="p-1 rounded-lg text-muted-foreground hover:text-foreground hover:bg-muted transition-colors"
                    aria-label="Fermer"
                  >
                    <X className="h-5 w-5" />
                  </button>
                )}
              </div>
            )}

            {/* Content */}
            <div className="p-5">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>,
    document.body
  )
}

export function ModalFooter({ className, children }) {
  return (
    <div
      className={cn(
        'flex items-center justify-end gap-3 pt-4 border-t border-border -mx-5 -mb-5 px-5 py-4 bg-muted/30 rounded-b-xl',
        className
      )}
    >
      {children}
    </div>
  )
}
