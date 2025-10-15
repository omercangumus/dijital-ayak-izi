import React, { useState, useEffect } from 'react';

const IntroPrompt = ({ onComplete, onGoogleAPIs }) => {
  const [currentText, setCurrentText] = useState('');
  const [currentLine, setCurrentLine] = useState(0);
  const [showCursor, setShowCursor] = useState(true);
  const [isComplete, setIsComplete] = useState(false);
  const [showSkipHint, setShowSkipHint] = useState(false);

  const introLines = [
    'INITIALIZING ADVANCED OSINT PLATFORM...',
    'LOADING GOOGLE DORKING ENGINE...',
    'ESTABLISHING SECURE CONNECTION... [200]',
    'LOADING PROFILE ANALYSIS MODULES... [OK]',
    'REVERSE IMAGE SEARCH ACTIVATED... [READY]',
    'USERNAME EXPANSION MODULE LOADED... [OK]',
    'ETHICAL FRAMEWORK VERIFIED... [KVKK/GDPR]',
    'ACCESS GRANTED.',
    '',
    '// &gt; OSINT PROFESSIONAL TOOL READY'
  ];

  useEffect(() => {
    const timer = setInterval(() => {
      if (currentLine < introLines.length) {
        const line = introLines[currentLine];
        if (currentText.length < line.length) {
          setCurrentText(currentText + line[currentText.length]);
        } else {
          // Line complete, move to next
          setTimeout(() => {
            setCurrentLine(currentLine + 1);
            setCurrentText('');
          }, 500);
        }
      } else {
        // All lines complete
        setIsComplete(true);
        clearInterval(timer);
        setTimeout(() => {
          onComplete();
        }, 1000);
      }
    }, 50);

    return () => clearInterval(timer);
  }, [currentText, currentLine, onComplete]);

  // Show skip hint after 2 seconds
  useEffect(() => {
    const hintTimer = setTimeout(() => {
      setShowSkipHint(true);
    }, 2000);

    return () => clearTimeout(hintTimer);
  }, []);

  // Handle keyboard events
  useEffect(() => {
    const handleKeyPress = (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        onComplete();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [onComplete]);

  // Blinking cursor effect
  useEffect(() => {
    const cursorTimer = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 530);

    return () => clearInterval(cursorTimer);
  }, []);

  return (
    <div className="space-y-1 relative">
      {/* Skip hint */}
      {showSkipHint && !isComplete && (
        <div className="absolute top-0 right-0 text-xs text-gray-500 animate-pulse">
          [ENTER veya SPACE tuşuna basarak geçin]
        </div>
      )}
      
      {introLines.slice(0, currentLine).map((line, index) => (
        <div key={index} className="text-green-400">
          {line}
        </div>
      ))}
      
      {currentLine < introLines.length && (
        <div className="text-green-400">
          {currentText}
          {showCursor && currentLine === introLines.length - 1 && '_'}
        </div>
      )}

      {isComplete && (
        <div className="text-green-400 animate-pulse">
          {currentText}
          {showCursor && '_'}
        </div>
      )}

      {isComplete && (
        <div className="mt-8 space-y-4">
          <div className="text-center">
            <button
              onClick={onComplete}
              className="bg-green-500 text-black px-6 py-3 rounded font-bold hover:bg-green-400 transition-colors mr-4"
            >
              OSINT ARAŞTIRMASI BAŞLAT
            </button>
            <button
              onClick={onGoogleAPIs}
              className="bg-blue-500 text-white px-6 py-3 rounded font-bold hover:bg-blue-400 transition-colors"
            >
              GOOGLE API'LERİ
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default IntroPrompt;
