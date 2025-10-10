import React, { useState } from 'react';

const Stage1SearchForm = ({ onSearchStart }) => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    city: ''
  });
  const [isSearching, setIsSearching] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.firstName || !formData.lastName || !formData.city) {
      return;
    }

    setIsSearching(true);
    try {
      const response = await fetch('http://localhost:8005/api/osint/stage1/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          firstName: formData.firstName,
          lastName: formData.lastName,
          city: formData.city
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const candidates = await response.json();
      await onSearchStart(formData, candidates);
    } catch (error) {
      console.error('Search error:', error);
      alert(`Arama hatası: ${error.message}`);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="space-y-6">
      {/* Ethical Warning */}
      <div className="border-l-2 border-red-500/50 pl-4 py-3 bg-red-500/5">
        <div className="text-red-400 text-sm font-mono tracking-wide">
          <div>[WARNING] PROFESSIONAL USE ONLY - KVKK/GDPR COMPLIANCE REQUIRED</div>
          <div>[WARNING] ONLY PUBLIC DATA WILL BE ACCESSED</div>
          <div>[WARNING] RESULTS ARE "POTENTIAL LEADS" NOT CONFIRMED FACTS</div>
        </div>
      </div>

      {/* Search Form */}
      <div className="bg-gray-900/50 border border-green-400/30 p-6 rounded">
        <h2 className="text-green-400 text-xl font-mono mb-6 tracking-wider">
          [STAGE 1] POTENTIAL PROFILE IDENTIFICATION
        </h2>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-green-400/80 text-sm font-mono mb-2">
                [FIELD] İsim (First Name)
              </label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleInputChange}
                className="w-full bg-gray-950 border border-green-400/50 text-green-400 px-3 py-2 font-mono focus:border-green-400 focus:outline-none"
                placeholder="Ahmet"
                required
              />
            </div>

            <div>
              <label className="block text-green-400/80 text-sm font-mono mb-2">
                [FIELD] Soyisim (Last Name)
              </label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleInputChange}
                className="w-full bg-gray-950 border border-green-400/50 text-green-400 px-3 py-2 font-mono focus:border-green-400 focus:outline-none"
                placeholder="Yılmaz"
                required
              />
            </div>

            <div>
              <label className="block text-green-400/80 text-sm font-mono mb-2">
                [FIELD] Memleket / Şehir (City)
              </label>
              <input
                type="text"
                name="city"
                value={formData.city}
                onChange={handleInputChange}
                className="w-full bg-gray-950 border border-green-400/50 text-green-400 px-3 py-2 font-mono focus:border-green-400 focus:outline-none"
                placeholder="Elazığ"
                required
              />
            </div>
          </div>

          <div className="pt-4">
            <button
              type="submit"
              disabled={isSearching}
              className="bg-green-400/10 border border-green-400 text-green-400 px-6 py-3 font-mono tracking-wider hover:bg-green-400/20 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSearching ? '[SCANNING...]' : '[POTANSİYEL PROFİLLERİ TARA]'}
            </button>
          </div>
        </form>
      </div>

      {/* Instructions */}
      <div className="text-green-400/60 text-sm font-mono space-y-1">
        <div>// &gt; Bu aşamada sadece potansiyel profiller taranacak</div>
        <div>// &gt; Bulunan sonuçlar "olası eşleşmeler" olarak gösterilecek</div>
        <div>// &gt; Doğru profili seçtikten sonra Stage 2 analizi başlayacak</div>
      </div>
    </div>
  );
};

export default Stage1SearchForm;
