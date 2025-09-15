import React, { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from '@/components/UI/Layout/Base'
import { Dashboard } from '@/components/Dashboard/Dashboard'
import { ThemeProvider } from './contexts/ThemeContext'
import { Navigation } from '@/components/Dashboard/Header/Navigation'
import { Modal } from '@/components/UI/Modal/Modal'
import SettingsPage from './components/Dashboard/settings/Settings'

const UIShowcase = () => <div className="p-4 text-sm text-gray-600">UI components showcase</div>

export default function App() {
  const [showImport, setShowImport] = useState(false)
  const [showSettings, setShowSettings] = useState(false)

  return (
    <ThemeProvider>
      <Layout
        title="Prospect AI Dashboard"
        headerActions={
          <Navigation
            onOpenImport={() => setShowImport(true)}
            onOpenSettings={() => setShowSettings(s => !s)}
          />
        }
        footer={<div className="text-xs text-gray-500">© {new Date().getFullYear()} Prospect AI</div>}
      >
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/ui" element={<UIShowcase />} />
          <Route path="/settings" element={<SettingsPage />} />
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>

        <Modal open={showImport} onClose={() => setShowImport(false)} title="Import">
          Paste your leads here…
        </Modal>
      </Layout>
    </ThemeProvider>
  )
}