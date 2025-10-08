import React from 'react'
import { motion } from 'framer-motion'
import { ShieldCheck, Search } from 'lucide-react'
import WarningBox from '../components/WarningBox'
import SearchForm from '../components/SearchForm'
import ProfileSelectionModal from '../components/ProfileSelectionModal'

const HomePage = () => {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-2xl mx-auto"
      >
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="text-center mb-8"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-slate-100 mb-4">
            Dijital Ayak İzi
            <span className="block text-primary-400">Analiz Paneli</span>
          </h1>
          <p className="text-xl text-slate-400 max-w-lg mx-auto">
            Çevrimiçi varlığınızı keşfedin ve yönetin.
          </p>
        </motion.div>

        {/* Warning Box */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="mb-8"
        >
          <WarningBox />
        </motion.div>

        {/* Search Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
          className="mb-8"
        >
          <SearchForm />
        </motion.div>

        {/* Profile Selection Modal */}
        <ProfileSelectionModal />
      </motion.div>
    </div>
  )
}

export default HomePage
