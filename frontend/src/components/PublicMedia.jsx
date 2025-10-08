import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Image, ExternalLink, Calendar, Eye, EyeOff } from 'lucide-react'

const PublicMedia = ({ analysisData }) => {
  const [showAll, setShowAll] = useState(false)
  const [selectedPhoto, setSelectedPhoto] = useState(null)

  const publicPhotos = analysisData?.public_photos || []

  const displayedPhotos = showAll ? publicPhotos : publicPhotos.slice(0, 8)

  const formatDate = (dateString) => {
    if (!dateString) return 'Tarih bilinmiyor'
    try {
      const date = new Date(dateString)
      return date.toLocaleDateString('tr-TR')
    } catch {
      return 'Tarih bilinmiyor'
    }
  }

  if (publicPhotos.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="card"
      >
        <div className="flex items-center space-x-3 mb-4">
          <Image className="h-6 w-6 text-primary-400" />
          <h3 className="text-lg font-semibold text-slate-200">Halka Açık Fotoğraflar</h3>
        </div>
        <div className="text-center py-8">
          <Image className="h-12 w-12 text-slate-400 mx-auto mb-4" />
          <p className="text-slate-400">Hiç halka açık fotoğraf bulunamadı</p>
        </div>
      </motion.div>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Image className="h-6 w-6 text-primary-400" />
          <h3 className="text-lg font-semibold text-slate-200">Halka Açık Fotoğraflar</h3>
          <span className="bg-primary-900 text-primary-400 px-2 py-1 rounded-full text-xs font-medium">
            {publicPhotos.length}
          </span>
        </div>
        {publicPhotos.length > 8 && (
          <motion.button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center space-x-2 text-sm text-primary-400 hover:text-primary-300 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {showAll ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            <span>{showAll ? 'Gizle' : `Tümünü Gör (${publicPhotos.length})`}</span>
          </motion.button>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        {displayedPhotos.map((photo, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="relative group cursor-pointer"
            onClick={() => setSelectedPhoto(photo)}
          >
            <div className="aspect-square rounded-lg overflow-hidden bg-slate-800 border border-slate-700">
              <img
                src={photo.thumbnail || photo.url}
                alt={photo.caption || 'Halka açık fotoğraf'}
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-200"
                onError={(e) => {
                  e.target.style.display = 'none'
                  e.target.nextSibling.style.display = 'flex'
                }}
              />
              <div className="w-full h-full flex items-center justify-center bg-slate-800" style={{ display: 'none' }}>
                <Image className="h-8 w-8 text-slate-400" />
              </div>
            </div>

            {/* Date badge */}
            {photo.date && (
              <div className="absolute bottom-2 left-2 px-2 py-1 bg-black/50 rounded text-xs text-white">
                {formatDate(photo.date)}
              </div>
            )}

            {/* Hover overlay */}
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex items-center justify-center">
              <ExternalLink className="h-6 w-6 text-white" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Photo Modal */}
      {selectedPhoto && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedPhoto(null)}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="bg-slate-800 rounded-xl max-w-4xl max-h-[80vh] overflow-hidden"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-6 border-b border-slate-700">
              <h3 className="text-xl font-semibold text-slate-200 mb-2">
                {selectedPhoto.caption || 'Halka Açık Fotoğraf'}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-slate-400">
                <div className="flex items-center space-x-2">
                  <Calendar className="h-4 w-4" />
                  <span>{formatDate(selectedPhoto.date)}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Image className="h-4 w-4" />
                  <span>Halka Açık</span>
                </div>
              </div>
            </div>
            
            <div className="p-6">
              <img
                src={selectedPhoto.url}
                alt={selectedPhoto.caption || 'Halka açık fotoğraf'}
                className="w-full max-h-96 object-contain rounded-lg"
              />
              
              <div className="mt-4 flex justify-end">
                <motion.a
                  href={selectedPhoto.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary flex items-center space-x-2"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>Orijinal Boyutta Görüntüle</span>
                </motion.a>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}

      {/* Summary */}
      {publicPhotos.length > 0 && (
        <div className="mt-6 pt-4 border-t border-slate-700">
          <div className="flex items-center justify-between text-sm text-slate-400">
            <span>
              Toplam {publicPhotos.length} halka açık fotoğraf bulundu
            </span>
            <span>
              Bu fotoğraflar herkese açık olarak paylaşılmıştır
            </span>
          </div>
        </div>
      )}
    </motion.div>
  )
}

export default PublicMedia
