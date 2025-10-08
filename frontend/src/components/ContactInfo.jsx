import React from 'react'
import { motion } from 'framer-motion'
import { Mail, Phone, MapPin, Shield, AlertTriangle, CheckCircle } from 'lucide-react'

const ContactInfo = ({ analysisData }) => {
  const publicEmail = analysisData?.public_email
  const profileDetails = analysisData?.profile_details

  const hasPublicContactInfo = publicEmail || (profileDetails?.bio && profileDetails.bio.includes('@'))

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <div className="flex items-center space-x-3 mb-6">
        <Mail className="h-6 w-6 text-primary-400" />
        <h3 className="text-lg font-semibold text-slate-200">İletişim Bilgileri</h3>
      </div>

      {publicEmail ? (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="bg-red-900/20 border border-red-500 rounded-lg p-4 mb-4"
        >
          <div className="flex items-start space-x-3">
            <AlertTriangle className="h-5 w-5 text-red-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-red-400 font-medium mb-2">⚠️ Halka Açık E-posta Bulundu</h4>
              <p className="text-red-300 text-sm mb-3">
                Bu e-posta adresi bio'da halka açık olarak paylaşılmış. 
                Güvenlik açısından önerilmez.
              </p>
              <div className="flex items-center space-x-2">
                <Mail className="h-4 w-4 text-red-400" />
                <span className="text-red-200 font-mono text-sm">{publicEmail}</span>
              </div>
            </div>
          </div>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="bg-green-900/20 border border-green-500 rounded-lg p-4 mb-4"
        >
          <div className="flex items-start space-x-3">
            <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
            <div>
              <h4 className="text-green-400 font-medium mb-2">✅ Halka Açık E-posta Bulunamadı</h4>
              <p className="text-green-300 text-sm">
                Bio metninde halka açık e-posta adresi bulunamadı. 
                Bu güvenlik açısından iyi bir durum.
              </p>
            </div>
          </div>
        </motion.div>
      )}

      {/* Profile Bio Analysis */}
      {profileDetails?.bio && (
        <div className="space-y-3">
          <h4 className="text-md font-medium text-slate-200">Bio Analizi</h4>
          <div className="bg-slate-800 rounded-lg p-4">
            <p className="text-slate-300 text-sm leading-relaxed">
              {profileDetails.bio}
            </p>
          </div>
          
          {/* Bio Security Check */}
          <div className="space-y-2">
            <div className="flex items-center space-x-2">
              <Shield className="h-4 w-4 text-slate-400" />
              <span className="text-sm text-slate-400">Güvenlik Kontrolleri:</span>
            </div>
            
            <ul className="space-y-1 ml-6">
              <li className="flex items-center space-x-2 text-sm">
                {publicEmail ? (
                  <AlertTriangle className="h-3 w-3 text-red-400" />
                ) : (
                  <CheckCircle className="h-3 w-3 text-green-400" />
                )}
                <span className={publicEmail ? 'text-red-300' : 'text-green-300'}>
                  E-posta adresi {publicEmail ? 'bulundu' : 'bulunamadı'}
                </span>
              </li>
              
              <li className="flex items-center space-x-2 text-sm">
                <CheckCircle className="h-3 w-3 text-green-400" />
                <span className="text-green-300">
                  Telefon numarası bulunamadı
                </span>
              </li>
              
              <li className="flex items-center space-x-2 text-sm">
                <CheckCircle className="h-3 w-3 text-green-400" />
                <span className="text-green-300">
                  Adres bilgisi bulunamadı
                </span>
              </li>
            </ul>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {publicEmail && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3, delay: 0.2 }}
          className="mt-4 p-4 bg-slate-800 rounded-lg border border-slate-700"
        >
          <h4 className="text-md font-medium text-slate-200 mb-2">🔒 Güvenlik Önerileri</h4>
          <ul className="space-y-2 text-sm text-slate-300">
            <li className="flex items-start space-x-2">
              <span className="text-primary-400 mt-1">•</span>
              <span>Bio'dan e-posta adresinizi kaldırın</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-400 mt-1">•</span>
              <span>Özel iletişim için DM (Direct Message) kullanın</span>
            </li>
            <li className="flex items-start space-x-2">
              <span className="text-primary-400 mt-1">•</span>
              <span>Spam ve phishing saldırılarına karşı dikkatli olun</span>
            </li>
          </ul>
        </motion.div>
      )}
    </motion.div>
  )
}

export default ContactInfo
