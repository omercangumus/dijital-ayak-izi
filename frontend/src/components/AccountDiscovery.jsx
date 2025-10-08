import React from 'react'
import { motion } from 'framer-motion'
import { Users, ExternalLink, CheckCircle, XCircle } from 'lucide-react'

const platformIcons = {
  github: '💻',
  twitter: '🐦',
  linkedin: '💼',
  instagram: '📷',
  facebook: '👥',
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

const AccountDiscovery = ({ analysisData }) => {
  const otherAccounts = analysisData?.other_accounts || []

  if (otherAccounts.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="card"
      >
        <div className="flex items-center space-x-3 mb-4">
          <Users className="h-6 w-6 text-primary-400" />
          <h3 className="text-lg font-semibold text-slate-200">Hesap Keşfi</h3>
        </div>
        <div className="text-center py-8">
          <XCircle className="h-12 w-12 text-slate-400 mx-auto mb-4" />
          <p className="text-slate-400">Hiçbir platformda hesap bulunamadı</p>
        </div>
      </motion.div>
    )
  }

  const getPlatformIcon = (platform) => {
    return platformIcons[platform?.toLowerCase()] || '🌐'
  }

  const getPlatformColor = (platform) => {
    const colors = {
      github: 'bg-gray-800',
      twitter: 'bg-blue-500',
      linkedin: 'bg-blue-600',
      instagram: 'bg-pink-500',
      facebook: 'bg-blue-700',
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
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="card"
    >
      <div className="flex items-center space-x-3 mb-6">
        <Users className="h-6 w-6 text-primary-400" />
        <h3 className="text-lg font-semibold text-slate-200">Hesap Keşfi</h3>
        <span className="bg-primary-900 text-primary-400 px-2 py-1 rounded-full text-xs font-medium">
          {otherAccounts.length}
        </span>
      </div>

      <div className="space-y-3">
        {otherAccounts.map((account, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="flex items-center justify-between p-3 bg-slate-800 rounded-lg border border-slate-700 hover:border-slate-600 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <div className={`w-10 h-10 rounded-full ${getPlatformColor(account.platform)} flex items-center justify-center text-white font-bold text-lg`}>
                {getPlatformIcon(account.platform)}
              </div>
              <div>
                <h4 className="text-slate-200 font-medium">{account.platform}</h4>
                {account.bio && (
                  <p className="text-sm text-slate-400 truncate max-w-48">
                    {account.bio}
                  </p>
                )}
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-400" />
                <span className="text-xs text-green-400">Aktif</span>
              </div>
              
              <motion.a
                href={account.url}
                target="_blank"
                rel="noopener noreferrer"
                className="p-2 hover:bg-slate-700 rounded-lg transition-colors"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <ExternalLink className="h-4 w-4 text-slate-400" />
              </motion.a>
            </div>
          </motion.div>
        ))}
      </div>

      {otherAccounts.length > 0 && (
        <div className="mt-4 pt-4 border-t border-slate-700">
          <p className="text-sm text-slate-400 text-center">
            Aynı kullanıcı adı ile {otherAccounts.length} farklı platformda hesap bulundu
          </p>
        </div>
      )}
    </motion.div>
  )
}

export default AccountDiscovery
