import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import ReportPage from './pages/ReportPage'
import { SearchProvider } from './context/SearchContext'

function App() {
  return (
    <SearchProvider>
      <Router>
        <div className="min-h-screen bg-slate-900">
          <AnimatePresence mode="wait">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/report" element={<ReportPage />} />
            </Routes>
          </AnimatePresence>
        </div>
      </Router>
    </SearchProvider>
  )
}

export default App
