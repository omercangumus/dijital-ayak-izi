import React, { useState, useEffect } from 'react';

const CliError = ({ error, onRetry }) => {
  const [showGlitch, setShowGlitch] = useState(false);

  useEffect(() => {
    // Random glitch effect
    const glitchInterval = setInterval(() => {
      setShowGlitch(true);
      setTimeout(() => setShowGlitch(false), 100);
    }, Math.random() * 3000 + 2000);

    return () => clearInterval(glitchInterval);
  }, []);

  const getErrorCode = (error) => {
    if (error.includes('401')) return 'UNAUTHORIZED';
    if (error.includes('404')) return 'NOT_FOUND';
    if (error.includes('500')) return 'SERVER_ERROR';
    if (error.includes('timeout')) return 'TIMEOUT';
    return 'UNKNOWN_ERROR';
  };

  const getErrorSuggestion = (errorCode) => {
    switch (errorCode) {
      case 'UNAUTHORIZED':
        return 'Please verify API keys in configuration.';
      case 'NOT_FOUND':
        return 'Target profile not found or URL is invalid.';
      case 'SERVER_ERROR':
        return 'Backend service is temporarily unavailable.';
      case 'TIMEOUT':
        return 'Request timed out. Please try again.';
      default:
        return 'Please check your connection and try again.';
    }
  };

  const errorCode = getErrorCode(error);
  const suggestion = getErrorSuggestion(errorCode);

  return (
    <div className={`space-y-4 ${showGlitch ? 'animate-pulse' : ''}`}>
      <div className="border-l-2 border-red-500/50 pl-4 py-2 bg-red-500/5">
        <div className="text-red-400 text-sm font-mono tracking-wide">
          <div>[ERROR] SYSTEM FAILURE: Could not retrieve data.</div>
          <div>[ERROR_CODE] {errorCode}</div>
          <div>[DETAILS] {error}</div>
          <div>[SUGGESTION] {suggestion}</div>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <button
          onClick={onRetry}
          className="text-green-400 hover:text-green-300 border border-green-400/50 px-4 py-2 hover:bg-green-400/10 transition-all duration-200 font-mono tracking-wider"
        >
          [RETRY]
        </button>
        <span className="text-green-400/60 text-sm">
          Press [RETRY] to attempt analysis again
        </span>
      </div>

      {/* Glitch Effect */}
      {showGlitch && (
        <div className="absolute inset-0 pointer-events-none">
          <div className="text-red-500/20 font-mono text-xs">
            SYSTEM_CORRUPTED...REBOOT_REQUIRED...
          </div>
        </div>
      )}
    </div>
  );
};

export default CliError;
