import axios from 'axios'

const API_BASE_URL = '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('[API] Request error:', error)
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('[API] Response error:', error)
    return Promise.reject(error)
  }
)

// Profile Analysis API functions
export const searchSocialMedia = async (name, platform = null) => {
  try {
    const response = await api.post('/profile-analysis/search-social-media', {
      name,
      platform
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Sosyal medya arama başarısız')
  }
}

export const analyzeProfile = async (profileUrl) => {
  try {
    const response = await api.post('/profile-analysis/analyze-profile', {
      profile_url: profileUrl
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Profil analizi başarısız')
  }
}

export const reverseImageSearch = async (imageUrl) => {
  try {
    const response = await api.post('/profile-analysis/reverse-image-search', {
      image_url: imageUrl
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Ters görsel arama başarısız')
  }
}

export const discoverOtherAccounts = async (username) => {
  try {
    const response = await api.post('/profile-analysis/discover-other-accounts', {
      username
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Hesap keşfi başarısız')
  }
}

export const findPublicEmail = async (bioText) => {
  try {
    const response = await api.post('/profile-analysis/find-public-email', {
      bio_text: bioText
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'E-posta çıkarma başarısız')
  }
}

export const listPublicPhotos = async (profileUrl) => {
  try {
    const response = await api.post('/profile-analysis/list-public-photos', {
      profile_url: profileUrl
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Fotoğraf listeleme başarısız')
  }
}

export const getEthicalGuidelines = async () => {
  try {
    const response = await api.get('/profile-analysis/ethical-guidelines')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Etik kılavuz alınamadı')
  }
}

export const getSupportedPlatforms = async () => {
  try {
    const response = await api.get('/profile-analysis/supported-platforms')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Desteklenen platformlar alınamadı')
  }
}

export const getHealthStatus = async () => {
  try {
    const response = await api.get('/profile-analysis/health')
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Sağlık kontrolü başarısız')
  }
}

// Legacy API functions (for backward compatibility)
export const doDetailedScan = async (fullName, email = null, confirmedLinks = []) => {
  try {
    const response = await api.post('/detailed-scan', {
      full_name: fullName,
      email,
      confirmed_links: confirmedLinks
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Detaylı tarama başarısız')
  }
}

export const doInitialScan = async (fullName, email = null) => {
  try {
    const response = await api.post('/initial-scan', {
      full_name: fullName,
      email
    })
    return response.data
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'İlk tarama başarısız')
  }
}

export default api
