import React, { ReactNode } from 'react'
import { Header } from '@/components/Dashboard/Header/Header'

type LayoutProps = {
  title?: string
  headerActions?: ReactNode   // like a named "block" for actions area
  children: ReactNode         // main "content" block
  footer?: ReactNode          // optional "footer" block
}

export const Layout: React.FC<LayoutProps> = ({ title, headerActions, children, footer }) => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {(title || headerActions) && (
          <div className="mb-4 flex items-center justify-between gap-4">
            {title ? <h1 className="text-xl font-semibold">{title}</h1> : <span />}
            {headerActions}
          </div>
        )}
        <main>{children}</main>
        {footer && <footer className="mt-8">{footer}</footer>}
      </div>
    </div>
  )
}