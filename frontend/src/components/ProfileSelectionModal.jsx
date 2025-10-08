import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { X, Check } from 'lucide-react'
import { useSearch } from '../context/SearchContext'
import ProfileCard from './ProfileCard'
import { useNavigate } from 'react-router-dom'
import { analyzeProfile } from '../services/api'

const ProfileSelectionModal = () => {
  const { 
    searchResults, 
    updateSearchResults, 
    selectProfile, 
    setLoading, 
    setErrorState 
  } = useSearch()
  const navigate = useNavigate()

  const handleProfileSelect = async (profile) => {
    try {
      setLoading(true)
      selectProfile(profile)
      
      // Analyze the selected profile
      const analysisData = await analyzeProfile(profile.profile_url)
      
      // Navigate to report page with data
      navigate('/report', { state: { profile, analysisData } })
    } catch (error) {
      setErrorState(error.message || 'Profil analizi başarısız')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    updateSearchResults(null)
  }

  if (!searchResults || !searchResults.profiles || searchResults.profiles.length === 0) {
    return null
  }

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
        onClick={handleClose}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          transition={{ duration: 0.3 }}
          className="bg-slate-800 rounded-xl shadow-2xl max-w-4xl w-full max-h-[80vh] overflow-hidden"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div className="flex items-center justify-between p-6 border-b border-slate-700">
            <div>
              <h2 className="text-2xl font-bold text-slate-200">
                Profil Seçimi
              </h2>
              <p className="text-slate-400 mt-1">
                Size ait olan profili seçin. Analiz edilecek profili belirleyin.
              </p>
            </div>
            <motion.button
              onClick={handleClose}
              className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <X className="h-6 w-6 text-slate-400" />
            </motion.button>
          </div>

          {/* Content */}
          <div className="p-6 overflow-y-auto max-h-[calc(80vh-120px)]">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {searchResults.profiles.map((profile, index) => (
                <motion.div
                  key={profile.profile_url}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                >
                  <ProfileCard
                    profile={profile}
                    onSelect={() => handleProfileSelect(profile)}
                  />
                </motion.div>
              ))}
            </div>

            {searchResults.profiles.length === 0 && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-12"
              >
                <div className="text-slate-400 mb-4">
                  <X className="h-12 w-12 mx-auto mb-2" />
                  <p>Hiç profil bulunamadı</p>
                </div>
              </motion.div>
            )}
          </div>

          {/* Footer */}
          <div className="p-6 border-t border-slate-700 bg-slate-900">
            <div className="flex items-center justify-between">
              <p className="text-sm text-slate-400">
                Toplam {searchResults.total_found} profil bulundu
              </p>
              <motion.button
                onClick={handleClose}
                className="btn-secondary"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                İptal
              </motion.button>
            </div>
          </div>
        </motion.div>
      </motion.div>
    </AnimatePresence>
  )
}

export default ProfileSelectionModal
