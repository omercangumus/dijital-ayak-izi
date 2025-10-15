import React, { useState } from 'react';
import IntroPrompt from './components/IntroPrompt';
import Stage1SearchForm from './components/Stage1SearchForm';
import CandidateResults from './components/CandidateResults';
import Stage2Dashboard from './components/Stage2Dashboard';
import GoogleAPIs from './components/GoogleAPIs';

function App() {
  const [appState, setAppState] = useState('intro'); // intro, stage1, stage2, google-apis
  const [searchData, setSearchData] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [isSearchingCandidates, setIsSearchingCandidates] = useState(false);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [error, setError] = useState(null);

  const handleIntroComplete = () => {
    setAppState('stage1');
  };

  // OSINT Stage 1 handlers
  const handleStage1Search = async (formData, candidatesData = null) => {
    setSearchData(formData);
    
    if (candidatesData) {
      setCandidates(candidatesData);
    } else {
      setIsSearchingCandidates(true);
      
      try {
        const response = await fetch('http://localhost:8005/api/osint/stage1/search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(formData),
        });
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const candidatesData = await response.json();
        setCandidates(candidatesData);
      } catch (err) {
        setError(err.message);
        console.error('Search error:', err);
      } finally {
        setIsSearchingCandidates(false);
      }
    }
  };

  const handleCandidateSelect = (candidate) => {
    setSelectedCandidate(candidate);
    setAppState('stage2');
  };

  const handleBackToStage1 = () => {
    setAppState('stage1');
    setSelectedCandidate(null);
  };

  const handleGoogleAPIs = () => {
    setAppState('google-apis');
  };

  return (
    <div className="min-h-screen bg-black text-green-400 font-mono p-8">
      <div className="max-w-4xl mx-auto">
        {/* Intro Animation */}
        {appState === 'intro' && (
          <IntroPrompt onComplete={handleIntroComplete} onGoogleAPIs={handleGoogleAPIs} />
        )}

        {/* OSINT Stage 1: Candidate Search */}
        {appState === 'stage1' && (
          <div className="space-y-6">
            <Stage1SearchForm 
              onSearchStart={handleStage1Search}
            />
            
            {error && (
              <div className="text-red-400 bg-red-900/20 p-4 rounded border border-red-400/30">
                <strong>Hata:</strong> {error}
              </div>
            )}
            
            {candidates.length > 0 && (
              <CandidateResults
                candidates={candidates}
                onCandidateSelect={handleCandidateSelect}
                isSearching={isSearchingCandidates}
              />
            )}
          </div>
        )}

        {/* OSINT Stage 2: Deep Analysis */}
        {appState === 'stage2' && selectedCandidate && (
          <Stage2Dashboard
            selectedCandidate={selectedCandidate}
            onBackToStage1={handleBackToStage1}
          />
        )}

        {/* Google APIs */}
        {appState === 'google-apis' && (
          <GoogleAPIs />
        )}
      </div>
    </div>
  );
}

export default App;