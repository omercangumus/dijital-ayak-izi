import React, { useState, useEffect } from 'react';

const IntroPrompt = ({ onComplete }) => {
  const [currentText, setCurrentText] = useState('');
  const [currentLine, setCurrentLine] = useState(0);
  const [showCursor, setShowCursor] = useState(true);
  const [isComplete, setIsComplete] = useState(false);

  const introLines = [
    'INITIALIZING CORE MODULES...',
    'LOADING KERNEL v4.2.0... [OK]',
    'ESTABLISHING SECURE CONNECTION... [200]',
    'LOADING DIGITAL FOOTPRINT DATABASE... [OK]',
    'SCANNER ENGINES ACTIVATED... [READY]',
    'ACCESS GRANTED.',
    '',
    '// &gt; '
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

  // Blinking cursor effect
  useEffect(() => {
    const cursorTimer = setInterval(() => {
      setShowCursor(prev => !prev);
    }, 530);

    return () => clearInterval(cursorTimer);
  }, []);

  return (
    <div className="space-y-1">
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
    </div>
  );
};

export default IntroPrompt;
