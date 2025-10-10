import React, { useState, useRef, useEffect } from 'react';

const SearchInput = ({ onSubmit, isAnalyzing }) => {
  const [inputValue, setInputValue] = useState('');
  const [showCursor, setShowCursor] = useState(true);
  const inputRef = useRef(null);

  // Blinking cursor effect
  useEffect(() => {
    const cursorTimer = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 530);
    return () => clearInterval(cursorTimer);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (inputValue.trim() && !isAnalyzing) {
      onSubmit(inputValue.trim());
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSubmit(e);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-2">
        <div className="flex items-center space-x-2">
          <span className="text-green-400">// &gt; ANALYZE_PROFILE --url=</span>
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="https://instagram.com/username"
            className="bg-transparent text-green-400 placeholder-green-400/50 border-none outline-none flex-1 font-mono"
            disabled={isAnalyzing}
          />
          {showCursor && !isAnalyzing && (
            <span className="text-green-400 animate-pulse">_</span>
          )}
        </div>
        
        {!isAnalyzing && (
          <div className="flex items-center space-x-4 text-sm">
            <button
              type="submit"
              className="text-green-400 hover:text-green-300 border border-green-400/50 px-3 py-1 hover:bg-green-400/10 transition-all duration-200 font-mono tracking-wider"
            >
              [EXECUTE]
            </button>
            <span className="text-green-400/60 text-xs">
              Press ENTER or click [EXECUTE]
            </span>
          </div>
        )}
      </form>

      {/* Ethical Warning */}
      <div className="border-l-2 border-red-500/50 pl-4 py-2 bg-red-500/5">
        <div className="text-red-400 text-sm font-mono tracking-wide">
          <div>[WARNING] THIS TOOL IS FOR PERSONAL DIGITAL FOOTPRINT DISCOVERY ONLY.</div>
          <div>[WARNING] UNAUTHORIZED USE IS STRICTLY PROHIBITED AND ILLEGAL.</div>
          <div>[WARNING] PROCEED WITH CAUTION.</div>
        </div>
      </div>
    </div>
  );
};

export default SearchInput;
