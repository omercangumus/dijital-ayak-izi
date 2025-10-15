import React, { useState } from 'react';
import { Search, MapPin, Youtube, Eye, Map, CheckCircle, XCircle } from 'lucide-react';

const GoogleAPIs = () => {
  const [activeTab, setActiveTab] = useState('youtube');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState({});
  const [query, setQuery] = useState('');
  const [location, setLocation] = useState('');

  const tabs = [
    { id: 'youtube', name: 'YouTube', icon: Youtube, color: 'text-red-500' },
    { id: 'places', name: 'Google Places', icon: MapPin, color: 'text-green-500' },
    { id: 'vision', name: 'Vision API', icon: Eye, color: 'text-blue-500' },
    { id: 'geocoding', name: 'Geocoding', icon: Map, color: 'text-purple-500' }
  ];

  const searchYouTube = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/google/youtube/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, max_results: 10 })
      });
      const data = await response.json();
      setResults({ ...results, youtube: data.results });
    } catch (error) {
      console.error('YouTube arama hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const searchPlaces = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/google/places/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, location, radius: 50000 })
      });
      const data = await response.json();
      setResults({ ...results, places: data.results });
    } catch (error) {
      console.error('Places arama hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const analyzeImage = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/google/vision/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image_url: query })
      });
      const data = await response.json();
      setResults({ ...results, vision: data.analysis });
    } catch (error) {
      console.error('Vision analiz hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const getGeolocation = async () => {
    if (!query.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('/api/google/geocoding/location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address: query })
      });
      const data = await response.json();
      setResults({ ...results, geocoding: data.location_info });
    } catch (error) {
      console.error('Geocoding hatası:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    switch (activeTab) {
      case 'youtube':
        searchYouTube();
        break;
      case 'places':
        searchPlaces();
        break;
      case 'vision':
        analyzeImage();
        break;
      case 'geocoding':
        getGeolocation();
        break;
    }
  };

  const renderYouTubeResults = () => {
    if (!results.youtube) return null;
    
    return (
      <div className="space-y-4">
        {results.youtube.map((video, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-4 border">
            <div className="flex gap-4">
              <img 
                src={video.thumbnail} 
                alt={video.title}
                className="w-32 h-24 object-cover rounded"
              />
              <div className="flex-1">
                <h3 className="font-semibold text-lg mb-2">{video.title}</h3>
                <p className="text-gray-600 text-sm mb-2 line-clamp-2">{video.description}</p>
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>👁️ {video.view_count} görüntülenme</span>
                  <span>👍 {video.like_count} beğeni</span>
                  <span>📅 {new Date(video.published_at).toLocaleDateString('tr-TR')}</span>
                </div>
                <a 
                  href={video.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="inline-block mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
                >
                  Videoyu İzle
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderPlacesResults = () => {
    if (!results.places) return null;
    
    return (
      <div className="space-y-4">
        {results.places.map((place, index) => (
          <div key={index} className="bg-white rounded-lg shadow-md p-4 border">
            <h3 className="font-semibold text-lg mb-2">{place.name}</h3>
            <p className="text-gray-600 mb-2">{place.address}</p>
            <div className="flex items-center gap-4 text-sm text-gray-500">
              <span>⭐ {place.rating}/5</span>
              <span>💰 {place.price_level > 0 ? '₺'.repeat(place.price_level) : 'Fiyat bilgisi yok'}</span>
              <span>📍 {place.types.join(', ')}</span>
            </div>
          </div>
        ))}
      </div>
    );
  };

  const renderVisionResults = () => {
    if (!results.vision) return null;
    
    return (
      <div className="space-y-4">
        <div className="bg-white rounded-lg shadow-md p-4 border">
          <h3 className="font-semibold text-lg mb-4">Görsel Analiz Sonuçları</h3>
          
          {results.vision.labels && results.vision.labels.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2">🏷️ Etiketler:</h4>
              <div className="flex flex-wrap gap-2">
                {results.vision.labels.map((label, index) => (
                  <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                    {label.description} ({Math.round(label.score * 100)}%)
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {results.vision.faces && results.vision.faces.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2">👤 Yüz Analizi:</h4>
              <div className="space-y-2">
                {results.vision.faces.map((face, index) => (
                  <div key={index} className="text-sm">
                    <span className="text-green-600">😊 Mutluluk: {face.joy_likelihood}</span>
                    <span className="text-red-600 ml-4">😢 Üzüntü: {face.sorrow_likelihood}</span>
                    <span className="text-orange-600 ml-4">😠 Öfke: {face.anger_likelihood}</span>
                    <span className="text-yellow-600 ml-4">😲 Şaşkınlık: {face.surprise_likelihood}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {results.vision.text && results.vision.text.length > 0 && (
            <div className="mb-4">
              <h4 className="font-medium mb-2">📝 Metin:</h4>
              <div className="bg-gray-100 p-3 rounded">
                {results.vision.text.map((text, index) => (
                  <p key={index} className="text-sm">{text.description}</p>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    );
  };

  const renderGeocodingResults = () => {
    if (!results.geocoding) return null;
    
    return (
      <div className="bg-white rounded-lg shadow-md p-4 border">
        <h3 className="font-semibold text-lg mb-4">Konum Bilgileri</h3>
        <div className="space-y-2">
          <p><strong>Adres:</strong> {results.geocoding.formatted_address}</p>
          <p><strong>Enlem:</strong> {results.geocoding.latitude}</p>
          <p><strong>Boylam:</strong> {results.geocoding.longitude}</p>
          <p><strong>Place ID:</strong> {results.geocoding.place_id}</p>
          <p><strong>Türler:</strong> {results.geocoding.types.join(', ')}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-6xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Google API'leri</h1>
        <p className="text-gray-600">YouTube, Places, Vision ve Geocoding API'leri ile gelişmiş arama</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex space-x-1 mb-6 bg-gray-100 p-1 rounded-lg">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-md transition-colors ${
                activeTab === tab.id
                  ? 'bg-white shadow-sm'
                  : 'hover:bg-gray-200'
              }`}
            >
              <Icon className={`w-4 h-4 ${tab.color}`} />
              <span className="font-medium">{tab.name}</span>
            </button>
          );
        })}
      </div>

      {/* Search Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex gap-4 mb-4">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              {activeTab === 'vision' ? 'Görsel URL' : 'Arama Terimi'}
            </label>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={
                activeTab === 'vision' 
                  ? 'https://example.com/image.jpg' 
                  : 'Arama terimi girin...'
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          {activeTab === 'places' && (
            <div className="w-64">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Konum (opsiyonel)
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="İstanbul, Türkiye"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          )}
        </div>
        
        <button
          onClick={handleSearch}
          disabled={loading || !query.trim()}
          className="bg-blue-500 text-white px-6 py-2 rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
              Aranıyor...
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              Ara
            </>
          )}
        </button>
      </div>

      {/* Results */}
      <div className="space-y-6">
        {activeTab === 'youtube' && renderYouTubeResults()}
        {activeTab === 'places' && renderPlacesResults()}
        {activeTab === 'vision' && renderVisionResults()}
        {activeTab === 'geocoding' && renderGeocodingResults()}
      </div>
    </div>
  );
};

export default GoogleAPIs;
