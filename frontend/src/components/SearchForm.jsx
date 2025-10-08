import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Search, Loader2, Instagram, Twitter, Linkedin, Github, Youtube } from 'lucide-react'
import { useSearch } from '../context/SearchContext'
import { searchSocialMedia } from '../services/api'

const platformOptions = [
  { value: '', label: 'Tüm Platformlar', icon: null },
  { value: 'twitter', label: 'X (Twitter)', icon: Twitter },
  { value: 'linkedin', label: 'LinkedIn', icon: Linkedin },
  { value: 'instagram', label: 'Instagram', icon: Instagram },
  { value: 'github', label: 'GitHub', icon: Github },
  { value: 'youtube', label: 'YouTube', icon: Youtube },
]

const SearchForm = () => {
  const { setLoading, updateSearchResults, setErrorState } = useSearch()
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    platform: ''
  })

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.firstName.trim() || !formData.lastName.trim()) {
      setErrorState('Lütfen ad ve soyad alanlarını doldurun.')
      return
    }

    const fullName = `${formData.firstName.trim()} ${formData.lastName.trim()}`
    
    try {
      setLoading(true)
      const results = await searchSocialMedia(fullName, formData.platform || null)
      updateSearchResults(results)
    } catch (error) {
      setErrorState(error.message || 'Arama sırasında bir hata oluştu.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <h2 className="text-2xl font-semibold text-slate-200 mb-6">
        Profil Arama
      </h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="firstName" className="block text-sm font-medium text-slate-300 mb-2">
              İsim
            </label>
            <input
              type="text"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleInputChange}
              className="input-field w-full"
              placeholder="Adınızı girin"
              required
            />
          </div>
          
          <div>
            <label htmlFor="lastName" className="block text-sm font-medium text-slate-300 mb-2">
              Soyisim
            </label>
            <input
              type="text"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleInputChange}
              className="input-field w-full"
              placeholder="Soyadınızı girin"
              required
            />
          </div>
        </div>

        <div>
          <label htmlFor="platform" className="block text-sm font-medium text-slate-300 mb-2">
            Sosyal Medya Platformu
          </label>
          <div className="relative">
            <select
              id="platform"
              name="platform"
              value={formData.platform}
              onChange={handleInputChange}
              className="input-field w-full appearance-none pr-10"
            >
              {platformOptions.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
              <Search className="h-4 w-4 text-slate-400" />
            </div>
          </div>
        </div>

        <motion.button
          type="submit"
          className="btn-primary w-full flex items-center justify-center space-x-2"
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Search className="h-5 w-5" />
          <span>Analizi Başlat</span>
        </motion.button>
      </form>
    </motion.div>
  )
}

export default SearchForm
