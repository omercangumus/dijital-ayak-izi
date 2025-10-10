import React, { useState } from 'react';

const CandidateResults = ({ candidates, onCandidateSelect, isSearching }) => {
  const [selectedCandidate, setSelectedCandidate] = useState(null);

  const handleSelect = (candidate) => {
    setSelectedCandidate(candidate);
    onCandidateSelect(candidate);
  };

  const getSourceIcon = (source) => {
    const icons = {
      'LinkedIn': '💼',
      'Facebook': '📘',
      'Twitter': '🐦',
      'Instagram': '📷',
      'YouTube': '📺',
      'GitHub': '💻',
      'Other': '🌐'
    };
    return icons[source] || icons['Other'];
  };

  const getSourceColor = (source) => {
    const colors = {
      'LinkedIn': 'text-blue-400',
      'Facebook': 'text-blue-600',
      'Twitter': 'text-blue-300',
      'Instagram': 'text-pink-400',
      'YouTube': 'text-red-500',
      'GitHub': 'text-gray-300',
      'Other': 'text-green-400'
    };
    return colors[source] || colors['Other'];
  };

  if (isSearching) {
    return (
      <div className="space-y-4">
        <div className="text-green-400 font-mono text-lg">
          [STATUS] Scanning for potential profiles...
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="bg-gray-900/30 border border-green-400/20 p-4 rounded animate-pulse">
              <div className="w-16 h-16 bg-gray-700 rounded-full mb-3"></div>
              <div className="h-4 bg-gray-700 rounded mb-2"></div>
              <div className="h-3 bg-gray-700 rounded mb-2"></div>
              <div className="h-3 bg-gray-700 rounded w-3/4"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (!candidates || candidates.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-green-400/60 font-mono text-lg mb-4">
          [RESULT] No potential profiles found
        </div>
        <div className="text-green-400/40 text-sm">
          Try different search terms or check spelling
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div className="text-green-400 font-mono text-lg">
          [RESULT] Found {candidates.length} potential profiles
        </div>
        <div className="text-green-400/60 text-sm font-mono">
          Select one to proceed to Stage 2
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {candidates.map((candidate, index) => (
          <div
            key={index}
            onClick={() => handleSelect(candidate)}
            className={`bg-gray-900/50 border-2 p-4 rounded cursor-pointer transition-all duration-200 hover:border-green-400/60 hover:bg-gray-900/70 ${
              selectedCandidate === candidate 
                ? 'border-green-400 bg-green-400/5' 
                : 'border-green-400/30'
            }`}
          >
            {/* Profile Picture */}
            <div className="flex items-start space-x-4 mb-3">
              <div className="w-16 h-16 rounded-full overflow-hidden bg-gray-700 flex items-center justify-center">
                {candidate.profile_pic_url ? (
                  <img
                    src={candidate.profile_pic_url}
                    alt="Profile"
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'flex';
                    }}
                  />
                ) : null}
                <div className="w-full h-full bg-gray-700 flex items-center justify-center text-2xl" style={{display: candidate.profile_pic_url ? 'none' : 'flex'}}>
                  {getSourceIcon(candidate.source)}
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-2 mb-1">
                  <span className={`font-mono text-sm ${getSourceColor(candidate.source)}`}>
                    {candidate.source}
                  </span>
                  <span className="text-green-400/60 text-xs">
                    #{index + 1}
                  </span>
                </div>
              </div>
            </div>

            {/* Name */}
            <div className="text-green-400 font-mono text-lg mb-2 truncate">
              {candidate.name}
            </div>

            {/* Snippet */}
            <div className="text-green-400/80 text-sm font-mono line-clamp-3 mb-3">
              {candidate.snippet}
            </div>

            {/* URL */}
            <div className="text-green-400/60 text-xs font-mono truncate">
              {candidate.profile_url}
            </div>

            {/* Selection Indicator */}
            {selectedCandidate === candidate && (
              <div className="mt-3 text-center">
                <div className="text-green-400 font-mono text-sm border border-green-400 px-3 py-1 rounded">
                  [SELECTED]
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Action Button */}
      {selectedCandidate && (
        <div className="text-center pt-6">
          <button
            onClick={() => onCandidateSelect(selectedCandidate)}
            className="bg-green-400/10 border border-green-400 text-green-400 px-8 py-3 font-mono tracking-wider hover:bg-green-400/20 transition-all duration-200"
          >
            [PROCEED TO STAGE 2 - DEEP ANALYSIS]
          </button>
        </div>
      )}
    </div>
  );
};

export default CandidateResults;
