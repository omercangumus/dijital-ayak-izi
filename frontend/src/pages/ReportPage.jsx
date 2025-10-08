import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useLocation, useNavigate } from 'react-router-dom'
import { ArrowLeft, RefreshCw } from 'lucide-react'
import SummaryCard from '../components/SummaryCard'
import VisualFootprint from '../components/VisualFootprint'
import AccountDiscovery from '../components/AccountDiscovery'
import ContactInfo from '../components/ContactInfo'
import PublicMedia from '../components/PublicMedia'
import RiskAssessment from '../components/RiskAssessment'

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
}

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: "easeOut"
    }
  }
}

const ReportPage = () => {
  const location = useLocation()
  const navigate = useNavigate()
  const [analysisData, setAnalysisData] = useState(null)
  const [profile, setProfile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)

  useEffect(() => {
    if (location.state) {
      setProfile(location.state.profile)
      setAnalysisData(location.state.analysisData)
    } else {
      // Redirect to home if no data
      navigate('/')
    }
  }, [location.state, navigate])

  const handleBackToHome = () => {
    navigate('/')
  }

  const handleRefreshAnalysis = async () => {
    if (!profile) return
    
    setIsLoading(true)
    try {
      // Re-analyze the profile
      const { analyzeProfile } = await import('../services/api')
      const newAnalysisData = await analyzeProfile(profile.profile_url)
      setAnalysisData(newAnalysisData)
    } catch (error) {
      console.error('Analysis refresh failed:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (!analysisData || !profile) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner mx-auto mb-4"></div>
          <p className="text-slate-400">Analiz verileri yükleniyor...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-slate-900 py-8">
      <div className="max-w-7xl mx-auto px-4">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <motion.button
                onClick={handleBackToHome}
                className="p-2 hover:bg-slate-800 rounded-lg transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <ArrowLeft className="h-6 w-6 text-slate-400" />
              </motion.button>
              <div>
                <h1 className="text-3xl font-bold text-slate-200">
                  Analiz Raporu
                </h1>
                <p className="text-slate-400 mt-1">
                  {profile.name} - Dijital Ayak İzi Analizi
                </p>
              </div>
            </div>
            
            <motion.button
              onClick={handleRefreshAnalysis}
              disabled={isLoading}
              className="btn-secondary flex items-center space-x-2"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <RefreshCw className={`h-4 w-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Yenile</span>
            </motion.button>
          </div>
        </motion.div>

        {/* Dashboard Grid */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="grid grid-cols-1 lg:grid-cols-3 gap-6"
        >
          {/* Summary Card - Full width on top */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-3"
          >
            <SummaryCard profile={profile} analysisData={analysisData} />
          </motion.div>

          {/* Risk Assessment */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-1"
          >
            <RiskAssessment analysisData={analysisData} />
          </motion.div>

          {/* Contact Info */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-1"
          >
            <ContactInfo analysisData={analysisData} />
          </motion.div>

          {/* Account Discovery */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-1"
          >
            <AccountDiscovery analysisData={analysisData} />
          </motion.div>

          {/* Visual Footprint */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-2"
          >
            <VisualFootprint analysisData={analysisData} />
          </motion.div>

          {/* Public Media */}
          <motion.div
            variants={itemVariants}
            className="lg:col-span-3"
          >
            <PublicMedia analysisData={analysisData} />
          </motion.div>
        </motion.div>
      </div>
    </div>
  )
}

export default ReportPage
