import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { Image, ExternalLink, Search, Eye, EyeOff } from 'lucide-react'

const VisualFootprint = ({ analysisData }) => {
  const [showAll, setShowAll] = useState(false)
  const [selectedImage, setSelectedImage] = useState(null)

  const reverseImageResults = analysisData?.reverse_image_results || []
  const publicPhotos = analysisData?.public_photos || []

  const allImages = [
    ...reverseImageResults.map(item => ({
      ...item,
      type: 'reverse_search',
      title: item.title || 'Ters Görsel Arama Sonucu',
      url: item.image_url || item.source_url,
      similarity: item.similarity_score
    })),
    ...publicPhotos.map(photo => ({
      ...photo,
      type: 'public_photo',
      title: photo.caption || 'Halka Açık Fotoğraf',
      url: photo.url,
      thumbnail: photo.thumbnail
    }))
  ]

  const displayedImages = showAll ? allImages : allImages.slice(0, 6)

  const getImageTypeColor = (type) => {
    switch (type) {
      case 'reverse_search':
        return 'bg-red-900/20 text-red-400 border-red-500'
      case 'public_photo':
        return 'bg-blue-900/20 text-blue-400 border-blue-500'
      default:
        return 'bg-slate-800 text-slate-400 border-slate-600'
    }
  }

  const getImageTypeIcon = (type) => {
    switch (type) {
      case 'reverse_search':
        return <Search className="h-3 w-3" />
      case 'public_photo':
        return <Image className="h-3 w-3" />
      default:
        return <Image className="h-3 w-3" />
    }
  }

  if (allImages.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="card"
      >
        <div className="flex items-center space-x-3 mb-4">
          <Image className="h-6 w-6 text-primary-400" />
          <h3 className="text-lg font-semibold text-slate-200">Görsel Ayak İzi</h3>
        </div>
        <div className="text-center py-8">
          <Image className="h-12 w-12 text-slate-400 mx-auto mb-4" />
          <p className="text-slate-400">Hiç görsel bulunamadı</p>
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
          <h3 className="text-lg font-semibold text-slate-200">Görsel Ayak İzi</h3>
        </div>
        {allImages.length > 6 && (
          <motion.button
            onClick={() => setShowAll(!showAll)}
            className="flex items-center space-x-2 text-sm text-primary-400 hover:text-primary-300 transition-colors"
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {showAll ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
            <span>{showAll ? 'Gizle' : `Tümünü Gör (${allImages.length})`}</span>
          </motion.button>
        )}
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {displayedImages.map((image, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="relative group cursor-pointer"
            onClick={() => setSelectedImage(image)}
          >
            <div className="aspect-square rounded-lg overflow-hidden bg-slate-800 border border-slate-700">
              <img
                src={image.thumbnail || image.url}
                alt={image.title}
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

            {/* Image type badge */}
            <div className={`absolute top-2 left-2 px-2 py-1 rounded-full text-xs font-medium border flex items-center space-x-1 ${getImageTypeColor(image.type)}`}>
              {getImageTypeIcon(image.type)}
              <span>{image.type === 'reverse_search' ? 'Ters Arama' : 'Halka Açık'}</span>
            </div>

            {/* Similarity score for reverse search */}
            {image.similarity && (
              <div className="absolute top-2 right-2 px-2 py-1 bg-black/50 rounded text-xs text-white">
                {Math.round(image.similarity * 100)}%
              </div>
            )}

            {/* Hover overlay */}
            <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-200 rounded-lg flex items-center justify-center">
              <ExternalLink className="h-6 w-6 text-white" />
            </div>
          </motion.div>
        ))}
      </div>

      {/* Image Modal */}
      {selectedImage && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/80 flex items-center justify-center p-4 z-50"
          onClick={() => setSelectedImage(null)}
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
                {selectedImage.title}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-slate-400">
                <span className={`px-2 py-1 rounded-full text-xs font-medium border flex items-center space-x-1 ${getImageTypeColor(selectedImage.type)}`}>
                  {getImageTypeIcon(selectedImage.type)}
                  <span>{selectedImage.type === 'reverse_search' ? 'Ters Görsel Arama' : 'Halka Açık Fotoğraf'}</span>
                </span>
                {selectedImage.similarity && (
                  <span>Benzerlik: {Math.round(selectedImage.similarity * 100)}%</span>
                )}
              </div>
            </div>
            
            <div className="p-6">
              <img
                src={selectedImage.url}
                alt={selectedImage.title}
                className="w-full max-h-96 object-contain rounded-lg"
              />
              
              <div className="mt-4 flex justify-end">
                <motion.a
                  href={selectedImage.source_url || selectedImage.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="btn-primary flex items-center space-x-2"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>Kaynağa Git</span>
                </motion.a>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  )
}

export default VisualFootprint
