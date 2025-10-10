import React, { useState, useEffect } from 'react';

const Stage2Dashboard = ({ selectedCandidate, onBackToStage1 }) => {
  const [analysisData, setAnalysisData] = useState({
    identity: { status: 'pending', data: null },
    contact: { status: 'pending', data: null },
    accounts: { status: 'pending', data: null },
    visualFootprint: { status: 'pending', data: null },
    publicGallery: { status: 'pending', data: null }
  });

  useEffect(() => {
    if (selectedCandidate) {
      startDeepAnalysis();
    }
  }, [selectedCandidate]);

  const startDeepAnalysis = async () => {
    // Simulate deep analysis process
    const modules = ['identity', 'contact', 'accounts', 'visualFootprint', 'publicGallery'];
    
    for (const module of modules) {
      setAnalysisData(prev => ({
        ...prev,
        [module]: { ...prev[module], status: 'analyzing' }
      }));

      // Simulate API call delay
      await new Promise(resolve => setTimeout(resolve, 2000));

      // Mock data for each module
      const mockData = getMockData(module);
      setAnalysisData(prev => ({
        ...prev,
        [module]: { status: 'complete', data: mockData }
      }));
    }
  };

  const getMockData = (module) => {
    switch (module) {
      case 'identity':
        return {
          fullName: selectedCandidate.name,
          username: '@ahmetyilmaz',
          bio: selectedCandidate.snippet,
          location: 'Elazığ, Turkey',
          website: 'https://ahmetyilmaz.dev'
        };
      case 'contact':
        return {
          foundEmails: ['ahmet.yilmaz@company.com', 'ayilmaz@university.edu'],
          guessedEmails: ['a.yilmaz@corp.com [GUESS]'],
          phoneNumbers: [],
          socialLinks: ['https://linkedin.com/in/ahmetyilmaz']
        };
      case 'accounts':
        return {
          platforms: [
            { name: 'GitHub', url: 'https://github.com/ahmetyilmaz', status: 'active' },
            { name: 'Stack Overflow', url: 'https://stackoverflow.com/users/123', status: 'active' },
            { name: 'Reddit', url: 'https://reddit.com/u/ahmetyilmaz', status: 'inactive' },
            { name: 'Medium', url: 'https://medium.com/@ahmetyilmaz', status: 'active' }
          ]
        };
      case 'visualFootprint':
        return {
          reverseImageResults: [
            { url: 'https://linkedin.com/in/ahmetyilmaz', platform: 'LinkedIn' },
            { url: 'https://github.com/ahmetyilmaz', platform: 'GitHub' },
            { url: 'https://company.com/team', platform: 'Company Website' }
          ]
        };
      case 'publicGallery':
        return {
          photos: [
            { url: 'https://example.com/photo1.jpg', description: 'Profile photo' },
            { url: 'https://example.com/photo2.jpg', description: 'Team photo' },
            { url: 'https://example.com/photo3.jpg', description: 'Event photo' }
          ]
        };
      default:
        return null;
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'pending': return '⏳';
      case 'analyzing': return '🔄';
      case 'complete': return '✅';
      case 'error': return '❌';
      default: return '❓';
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'pending': return 'text-gray-400';
      case 'analyzing': return 'text-yellow-400';
      case 'complete': return 'text-green-400';
      case 'error': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-green-400 text-2xl font-mono tracking-wider mb-2">
            [STAGE 2] DEEP ANALYSIS DASHBOARD
          </h2>
          <div className="text-green-400/60 font-mono text-sm">
            Target: {selectedCandidate.name} | Source: {selectedCandidate.source}
          </div>
        </div>
        <button
          onClick={onBackToStage1}
          className="text-green-400/60 hover:text-green-400 font-mono text-sm border border-green-400/50 px-3 py-1 hover:bg-green-400/10 transition-all duration-200"
        >
          [BACK TO STAGE 1]
        </button>
      </div>

      {/* Identity Information */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-2xl">{getStatusIcon(analysisData.identity.status)}</span>
          <h3 className="text-green-400 text-lg font-mono tracking-wider">
            [MODULE 1] Kimlik Bilgileri (Identity)
          </h3>
          <span className={`text-sm font-mono ${getStatusColor(analysisData.identity.status)}`}>
            {analysisData.identity.status.toUpperCase()}
          </span>
        </div>

        {analysisData.identity.status === 'analyzing' && (
          <div className="text-green-400/60 font-mono text-sm">
            [PROGRESS] Extracting profile data from {selectedCandidate.profile_url}...
          </div>
        )}

        {analysisData.identity.data && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-sm">
            <div>
              <span className="text-green-400/60">Full Name:</span>
              <span className="text-green-400 ml-2">{analysisData.identity.data.fullName}</span>
            </div>
            <div>
              <span className="text-green-400/60">Username:</span>
              <span className="text-green-400 ml-2">{analysisData.identity.data.username}</span>
            </div>
            <div className="md:col-span-2">
              <span className="text-green-400/60">Bio:</span>
              <div className="text-green-400 ml-2 mt-1">{analysisData.identity.data.bio}</div>
            </div>
            <div>
              <span className="text-green-400/60">Location:</span>
              <span className="text-green-400 ml-2">{analysisData.identity.data.location}</span>
            </div>
            <div>
              <span className="text-green-400/60">Website:</span>
              <span className="text-green-400 ml-2">{analysisData.identity.data.website}</span>
            </div>
          </div>
        )}
      </div>

      {/* Contact Information */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-2xl">{getStatusIcon(analysisData.contact.status)}</span>
          <h3 className="text-green-400 text-lg font-mono tracking-wider">
            [MODULE 2] Potansiyel İletişim (Contact)
          </h3>
          <span className={`text-sm font-mono ${getStatusColor(analysisData.contact.status)}`}>
            {analysisData.contact.status.toUpperCase()}
          </span>
        </div>

        {analysisData.contact.status === 'analyzing' && (
          <div className="text-green-400/60 font-mono text-sm">
            [PROGRESS] Searching for email addresses and contact information...
          </div>
        )}

        {analysisData.contact.data && (
          <div className="space-y-3 font-mono text-sm">
            <div>
              <span className="text-green-400/60">Found Emails:</span>
              <div className="text-green-400 ml-2 mt-1 space-y-1">
                {analysisData.contact.data.foundEmails.map((email, i) => (
                  <div key={i}>• {email}</div>
                ))}
              </div>
            </div>
            <div>
              <span className="text-yellow-400/60">Guessed Emails:</span>
              <div className="text-yellow-400 ml-2 mt-1 space-y-1">
                {analysisData.contact.data.guessedEmails.map((email, i) => (
                  <div key={i}>• {email}</div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Other Online Accounts */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-2xl">{getStatusIcon(analysisData.accounts.status)}</span>
          <h3 className="text-green-400 text-lg font-mono tracking-wider">
            [MODULE 3] Diğer Çevrimiçi Hesaplar (Online Accounts)
          </h3>
          <span className={`text-sm font-mono ${getStatusColor(analysisData.accounts.status)}`}>
            {analysisData.accounts.status.toUpperCase()}
          </span>
        </div>

        {analysisData.accounts.status === 'analyzing' && (
          <div className="text-green-400/60 font-mono text-sm">
            [PROGRESS] Checking username across multiple platforms...
          </div>
        )}

        {analysisData.accounts.data && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {analysisData.accounts.data.platforms.map((platform, i) => (
              <div key={i} className="bg-gray-800/50 border border-green-400/20 p-3 rounded text-center">
                <div className="text-2xl mb-2">💻</div>
                <div className="text-green-400 font-mono text-sm">{platform.name}</div>
                <div className={`text-xs font-mono ${
                  platform.status === 'active' ? 'text-green-400' : 'text-gray-400'
                }`}>
                  {platform.status}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Visual Footprint */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-2xl">{getStatusIcon(analysisData.visualFootprint.status)}</span>
          <h3 className="text-green-400 text-lg font-mono tracking-wider">
            [MODULE 4] Görsel Ayak İzi (Visual Footprint)
          </h3>
          <span className={`text-sm font-mono ${getStatusColor(analysisData.visualFootprint.status)}`}>
            {analysisData.visualFootprint.status.toUpperCase()}
          </span>
        </div>

        {analysisData.visualFootprint.status === 'analyzing' && (
          <div className="text-green-400/60 font-mono text-sm">
            [PROGRESS] Performing reverse image search on profile picture...
          </div>
        )}

        {analysisData.visualFootprint.data && (
          <div className="space-y-2 font-mono text-sm">
            {analysisData.visualFootprint.data.reverseImageResults.map((result, i) => (
              <div key={i} className="flex justify-between items-center bg-gray-800/30 p-2 rounded">
                <span className="text-green-400">{result.platform}</span>
                <span className="text-green-400/60 text-xs">{result.url}</span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Public Gallery */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <div className="flex items-center space-x-3 mb-4">
          <span className="text-2xl">{getStatusIcon(analysisData.publicGallery.status)}</span>
          <h3 className="text-green-400 text-lg font-mono tracking-wider">
            [MODULE 5] Herkese Açık Galeri (Public Gallery)
          </h3>
          <span className={`text-sm font-mono ${getStatusColor(analysisData.publicGallery.status)}`}>
            {analysisData.publicGallery.status.toUpperCase()}
          </span>
        </div>

        {analysisData.publicGallery.status === 'analyzing' && (
          <div className="text-green-400/60 font-mono text-sm">
            [PROGRESS] Collecting public photos from profile...
          </div>
        )}

        {analysisData.publicGallery.data && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {analysisData.publicGallery.data.photos.map((photo, i) => (
              <div key={i} className="bg-gray-800/30 border border-green-400/20 p-3 rounded">
                <div className="w-full h-32 bg-gray-700 rounded mb-2 flex items-center justify-center">
                  <span className="text-gray-400">📷</span>
                </div>
                <div className="text-green-400 font-mono text-xs text-center">
                  {photo.description}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Stage2Dashboard;
