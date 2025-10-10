import React, { useState } from 'react';
import TerminalShell from './components/TerminalShell';
import IntroPrompt from './components/IntroPrompt';
import SearchInput from './components/SearchInput';
import AnalysisOutput from './components/AnalysisOutput';
import CliError from './components/CliError';

function App() {
  const [appState, setAppState] = useState('intro'); // intro, ready, analyzing, complete, error
  const [currentUrl, setCurrentUrl] = useState('');
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const handleIntroComplete = () => {
    setAppState('ready');
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

        {/* Ready State - Show Input */}
        {(appState === 'ready' || appState === 'complete') && (
          <div className="space-y-6">
            <SearchInput 
              onSubmit={handleAnalysisStart}
              isAnalyzing={appState === 'analyzing'}
            />
            
            {/* Show new analysis button if completed */}
            {appState === 'complete' && (
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleNewAnalysis}
                  className="text-green-400 hover:text-green-300 border border-green-400/50 px-4 py-2 hover:bg-green-400/10 transition-all duration-200 font-mono tracking-wider"
                >
                  [NEW_ANALYSIS]
                </button>
                <span className="text-green-400/60 text-sm">
                  Ready for next analysis
                </span>
              </div>
            )}
          </div>
        )}

        {/* Analyzing State */}
        {appState === 'analyzing' && (
          <AnalysisOutput
            url={currentUrl}
            onComplete={handleAnalysisComplete}
            onError={handleAnalysisError}
          />
        )}

        {/* Error State */}
        {appState === 'error' && (
          <CliError 
            error={error} 
            onRetry={handleRetry}
          />
        )}

        {/* Terminal Prompt for Ready State */}
        {appState === 'ready' && (
          <div className="mt-8 text-green-400/60 text-sm">
            <div>// > Type a social media URL above and press ENTER to begin analysis</div>
            <div>// > Supported platforms: Instagram, Twitter, LinkedIn, Facebook</div>
          </div>
        )}
      </div>
    </TerminalShell>
  );
}

export default App;