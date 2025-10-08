import React from 'react'
import { motion } from 'framer-motion'
import { User, Shield, Clock, ExternalLink } from 'lucide-react'

const SummaryCard = ({ profile, analysisData }) => {
  const getRiskColor = (riskLevel) => {
    switch (riskLevel?.toLowerCase()) {
      case 'yüksek':
        return 'text-red-400 bg-red-900/20 border-red-500'
      case 'orta':
        return 'text-yellow-400 bg-yellow-900/20 border-yellow-500'
      case 'düşük':
        return 'text-green-400 bg-green-900/20 border-green-500'
      default:
        return 'text-slate-400 bg-slate-800 border-slate-600'
    }
  }

  const getRiskScore = () => {
    return analysisData?.risk_assessment?.risk_score || 0
  }

  const getRiskLevel = () => {
    return analysisData?.risk_assessment?.risk_level || 'Bilinmiyor'
  }

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Bilinmiyor'
    const date = new Date(timestamp * 1000)
    return date.toLocaleString('tr-TR')
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <div className="flex flex-col md:flex-row items-start md:items-center space-y-6 md:space-y-0 md:space-x-6">
        {/* Profile Picture */}
        <div className="flex-shrink-0">
          <div className="relative">
            {profile.profile_picture ? (
              <img
                src={profile.profile_picture}
                alt={profile.name}
                className="w-24 h-24 rounded-full object-cover border-4 border-slate-600"
              />
            ) : (
              <div className="w-24 h-24 rounded-full bg-slate-700 border-4 border-slate-600 flex items-center justify-center">
                <User className="h-12 w-12 text-slate-400" />
              </div>
            )}
            <div className="absolute -bottom-2 -right-2 w-8 h-8 bg-slate-800 rounded-full border-2 border-slate-700 flex items-center justify-center">
              <Shield className="h-4 w-4 text-primary-400" />
            </div>
          </div>
        </div>

        {/* Profile Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-3 mb-2">
            <h2 className="text-2xl font-bold text-slate-200 truncate">
              {profile.name}
            </h2>
            <a
              href={profile.profile_url}
              target="_blank"
              rel="noopener noreferrer"
              className="p-1 hover:bg-slate-700 rounded transition-colors"
            >
              <ExternalLink className="h-4 w-4 text-slate-400" />
            </a>
          </div>
          
          <p className="text-primary-400 mb-4">
            @{profile.username} • {profile.platform}
          </p>

          {profile.bio && (
            <p className="text-slate-300 mb-4 line-clamp-2">
              {profile.bio}
            </p>
          )}

          {/* Analysis Info */}
          <div className="flex flex-wrap items-center gap-4 text-sm text-slate-400">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4" />
              <span>Analiz: {formatTimestamp(analysisData?.analysis_timestamp)}</span>
            </div>
            <div className="flex items-center space-x-2">
              <span>Süre: {analysisData?.processing_time?.toFixed(2)}s</span>
            </div>
          </div>
        </div>

        {/* Risk Score */}
        <div className="flex-shrink-0">
          <div className="text-center">
            <div className={`inline-flex items-center px-4 py-2 rounded-full border ${getRiskColor(getRiskLevel())}`}>
              <Shield className="h-4 w-4 mr-2" />
              <span className="font-medium">{getRiskScore()}/100</span>
            </div>
            <p className="text-sm text-slate-400 mt-2">
              Gizlilik Skoru
            </p>
            <p className={`text-xs font-medium ${getRiskColor(getRiskLevel()).split(' ')[0]}`}>
              {getRiskLevel().toUpperCase()}
            </p>
          </div>
        </div>
      </div>

      {/* Additional Profile Details */}
      {analysisData?.profile_details && (
        <div className="mt-6 pt-6 border-t border-slate-700">
          <h3 className="text-lg font-semibold text-slate-200 mb-4">
            Profil Detayları
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <span className="text-sm text-slate-400">Platform:</span>
              <p className="text-slate-200 font-medium">
                {analysisData.profile_details.platform || 'Bilinmiyor'}
              </p>
            </div>
            <div>
              <span className="text-sm text-slate-400">Kullanıcı Adı:</span>
              <p className="text-slate-200 font-medium">
                {analysisData.profile_details.username || 'Bilinmiyor'}
              </p>
            </div>
            {analysisData.profile_details.full_name && (
              <div>
                <span className="text-sm text-slate-400">Tam Ad:</span>
                <p className="text-slate-200 font-medium">
                  {analysisData.profile_details.full_name}
                </p>
              </div>
            )}
            {analysisData.profile_details.verification_status && (
              <div>
                <span className="text-sm text-slate-400">Durum:</span>
                <p className="text-green-400 font-medium">
                  ✓ Doğrulanmış Hesap
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default SummaryCard
