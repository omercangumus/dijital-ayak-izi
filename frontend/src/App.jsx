import React, { useState } from 'react';
import TerminalShell from './components/TerminalShell';
import IntroPrompt from './components/IntroPrompt';
import SearchInput from './components/SearchInput';
import AnalysisOutput from './components/AnalysisOutput';
import CliError from './components/CliError';
import Stage1SearchForm from './components/Stage1SearchForm';
import CandidateResults from './components/CandidateResults';
import Stage2Dashboard from './components/Stage2Dashboard';

function App() {
  const [appState, setAppState] = useState('intro'); // intro, stage1, stage2, error
  const [currentUrl, setCurrentUrl] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);
  
  // OSINT Stage 1 state
  const [searchData, setSearchData] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [isSearchingCandidates, setIsSearchingCandidates] = useState(false);
  
  // OSINT Stage 2 state
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleIntroComplete = () => {
    setAppState('stage1');
  };

  // OSINT Stage 1 handlers
  const handleStage1Search = async (formData) => {
    setSearchData(formData);
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
      setAppState('error');
    } finally {
      setIsSearchingCandidates(false);
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

  const handleAnalysisStart = (url) => {
    setCurrentUrl(url);
    setAppState('analyzing');
    setError(null);
    setAnalysisResult(null);
  };

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result);
    setAppState('complete');
  };

  const handleAnalysisError = (err) => {
    setError(err.message);
    setAppState('error');
  };

  const handleRetry = () => {
    setAppState('ready');
    setError(null);
  };

  const handleNewAnalysis = () => {
    setAppState('ready');
    setCurrentUrl('');
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <TerminalShell>
      <div className="space-y-6">
        {/* Intro Animation */}
        {appState === 'intro' && (
          <IntroPrompt onComplete={handleIntroComplete} />
        )}

        {/* OSINT Stage 1: Candidate Search */}
        {appState === 'stage1' && (
          <div className="space-y-6">
            <Stage1SearchForm 
              onSearchStart={handleStage1Search}
            />
            
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

        {/* Error State */}
        {appState === 'error' && (
          <CliError 
            error={error} 
            onRetry={() => setAppState('stage1')}
          />
        )}
      </div>
    </TerminalShell>
  );
}

export default App;