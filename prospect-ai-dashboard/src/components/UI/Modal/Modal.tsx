import React, { useEffect, useRef } from 'react'

type ModalProps = {
  open: boolean
  onClose: () => void
  title?: string
  size?: 'sm' | 'md' | 'lg'
  children: React.ReactNode
}

export const Modal: React.FC<ModalProps> = ({ open, onClose, title, size = 'md', children }) => {
  const ref = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose() }
    document.addEventListener('keydown', onKey)
    ref.current?.focus()
    return () => document.removeEventListener('keydown', onKey)
  }, [open, onClose])

  if (!open) return null

  const sizeCls = size === 'sm' ? 'max-w-md' : size === 'lg' ? 'max-w-3xl' : 'max-w-xl'

  return (
    <div className="fixed inset-0 z-50" aria-labelledby="modal-title" role="dialog" aria-modal="true">
      <div className="fixed inset-0 bg-black/40" onClick={onClose} />
      <div className="fixed inset-0 flex items-center justify-center p-4">
        <div
          ref={ref}
          tabIndex={-1}
          className={`w-full ${sizeCls} rounded-lg bg-white dark:bg-gray-800 shadow-xl ring-1 ring-black/5 outline-none`}
          onClick={(e) => e.stopPropagation()}
        >
          <div className="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
            {title ? <h2 id="modal-title" className="text-base font-semibold">{title}</h2> : <span />}
            <button
              onClick={onClose}
              aria-label="Close"
              className="rounded p-1 hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <span aria-hidden="true">✕</span>
            </button>
          </div>
          <div className="p-4">{children}</div>
        </div>
      </div>
    </div>
  )
}

// export { Modal } from './Modal'