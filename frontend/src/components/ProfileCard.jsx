import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ExternalLink, User, Check } from 'lucide-react'

const platformIcons = {
  twitter: '🐦',
  linkedin: '💼',
  instagram: '📷',
  facebook: '👥',
  github: '💻',
  youtube: '📺',
  reddit: '🤖',
  tiktok: '🎵',
  pinterest: '📌',
  snapchat: '👻',
  medium: '📝',
  'dev.to': '💻',
  behance: '🎨',
  dribbble: '🏀',
  steam: '🎮',
  discord: '💬',
  telegram: '✈️',
  twitch: '🎮',
  vimeo: '🎬',
  soundcloud: '🎵',
  spotify: '🎵',
  'last.fm': '🎵',
  flickr: '📸',
  '500px': '📸',
  deviantart: '🎨',
  artstation: '🎨',
  codepen: '💻',
  stackoverflow: '💻',
  gitlab: '💻',
  bitbucket: '💻',
  keybase: '🔑',
  hackernews: '📰',
  producthunt: '🚀',
  angellist: '👼',
  crunchbase: '💼',
  slideshare: '📊',
  speakerdeck: '📊',
  mixcloud: '🎵',
  goodreads: '📚',
  letterboxd: '🎬',
  imdb: '🎬',
  researchgate: '🔬',
  academia: '🎓',
  orcid: '🔬',
  'google scholar': '🎓',
  mendeley: '📚',
  kaggle: '📊',
  hackerrank: '💻',
  leetcode: '💻',
  codeforces: '💻',
  atcoder: '💻',
  topcoder: '💻',
  codechef: '💻'
}

const ProfileCard = ({ profile, onSelect }) => {
  const [imageError, setImageError] = useState(false)
  const [isSelected, setIsSelected] = useState(false)

  const handleClick = () => {
    setIsSelected(true)
    setTimeout(() => {
      onSelect()
    }, 200)
  }

  const getPlatformIcon = (platform) => {
    return platformIcons[platform?.toLowerCase()] || '🌐'
  }

  const getPlatformColor = (platform) => {
    const colors = {
      twitter: 'bg-blue-500',
      linkedin: 'bg-blue-600',
      instagram: 'bg-pink-500',
      facebook: 'bg-blue-700',
      github: 'bg-gray-800',
      youtube: 'bg-red-600',
      reddit: 'bg-orange-500',
      tiktok: 'bg-black',
      pinterest: 'bg-red-500',
      snapchat: 'bg-yellow-400',
      medium: 'bg-green-500',
      'dev.to': 'bg-gray-700',
      behance: 'bg-blue-400',
      dribbble: 'bg-pink-400',
      steam: 'bg-blue-600',
      discord: 'bg-indigo-600',
      telegram: 'bg-blue-500',
      twitch: 'bg-purple-600',
      vimeo: 'bg-blue-500',
      soundcloud: 'bg-orange-500',
      spotify: 'bg-green-500',
      'last.fm': 'bg-red-500',
      flickr: 'bg-pink-500',
      '500px': 'bg-black',
      deviantart: 'bg-green-600',
      artstation: 'bg-blue-600',
      codepen: 'bg-black',
      stackoverflow: 'bg-orange-500',
      gitlab: 'bg-orange-600',
      bitbucket: 'bg-blue-700',
      keybase: 'bg-orange-500',
      hackernews: 'bg-orange-600',
      producthunt: 'bg-orange-500',
      angellist: 'bg-blue-600',
      crunchbase: 'bg-blue-600',
      slideshare: 'bg-blue-500',
      speakerdeck: 'bg-blue-600',
      mixcloud: 'bg-orange-500',
      goodreads: 'bg-brown-600',
      letterboxd: 'bg-blue-600',
      imdb: 'bg-yellow-500',
      researchgate: 'bg-green-600',
      academia: 'bg-blue-600',
      orcid: 'bg-green-600',
      'google scholar': 'bg-blue-600',
      mendeley: 'bg-blue-600',
      kaggle: 'bg-blue-600',
      hackerrank: 'bg-green-600',
      leetcode: 'bg-yellow-600',
      codeforces: 'bg-red-600',
      atcoder: 'bg-blue-600',
      topcoder: 'bg-red-600',
      codechef: 'bg-orange-600'
    }
    return colors[platform?.toLowerCase()] || 'bg-slate-600'
  }

  return (
    <motion.div
      className={`card cursor-pointer relative overflow-hidden transition-all duration-300 ${
        isSelected ? 'ring-2 ring-primary-500 bg-primary-900' : ''
      }`}
      onClick={handleClick}
      whileHover={{ scale: 1.02, y: -5 }}
      whileTap={{ scale: 0.98 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {/* Selection indicator */}
      {isSelected && (
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute top-3 right-3 z-10"
        >
          <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center">
            <Check className="h-5 w-5 text-white" />
          </div>
        </motion.div>
      )}

      {/* Platform badge */}
      <div className={`absolute top-3 left-3 px-2 py-1 rounded-full text-xs font-medium text-white ${getPlatformColor(profile.platform)}`}>
        <span className="mr-1">{getPlatformIcon(profile.platform)}</span>
        {profile.platform}
      </div>

      {/* Profile picture */}
      <div className="flex flex-col items-center text-center pt-8">
        <div className="relative mb-4">
          {profile.profile_picture && !imageError ? (
            <img
              src={profile.profile_picture}
              alt={profile.name}
              className="w-20 h-20 rounded-full object-cover border-4 border-slate-600"
              onError={() => setImageError(true)}
            />
          ) : (
            <div className="w-20 h-20 rounded-full bg-slate-700 border-4 border-slate-600 flex items-center justify-center">
              <User className="h-10 w-10 text-slate-400" />
            </div>
          )}
        </div>

        {/* Profile info */}
        <h3 className="text-lg font-semibold text-slate-200 mb-1">
          {profile.name}
        </h3>
        
        <p className="text-primary-400 mb-2">
          @{profile.username}
        </p>

        {profile.bio && (
          <p className="text-sm text-slate-400 mb-3 line-clamp-2">
            {profile.bio}
          </p>
        )}

        {/* Additional info */}
        <div className="flex items-center justify-center space-x-4 text-xs text-slate-500">
          {profile.followers && (
            <span>{profile.followers} takipçi</span>
          )}
          {profile.verified && (
            <span className="text-primary-400">✓ Doğrulanmış</span>
          )}
        </div>
      </div>

      {/* External link */}
      <div className="mt-4 pt-4 border-t border-slate-700">
        <div className="flex items-center justify-center space-x-2 text-primary-400 hover:text-primary-300 transition-colors">
          <ExternalLink className="h-4 w-4" />
          <span className="text-sm">Profili Görüntüle</span>
        </div>
      </div>
    </motion.div>
  )
}

export default ProfileCard
