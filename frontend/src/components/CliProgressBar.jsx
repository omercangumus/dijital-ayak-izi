import React, { useState, useEffect } from 'react';

const CliProgressBar = ({ progress = 0, text = "Progress" }) => {
  const [animatedProgress, setAnimatedProgress] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setAnimatedProgress((prev) => {
        if (prev < progress) {
          return Math.min(prev + 2, progress);
        }
        return prev;
      });
    }, 50);

    return () => clearInterval(interval);
  }, [progress]);

  const filledBlocks = Math.floor((animatedProgress / 100) * 10);
  const emptyBlocks = 10 - filledBlocks;

  return (
    <div className="flex items-center space-x-2">
      <span className="text-green-400 text-sm">{text}</span>
      <span className="text-green-400 font-mono">
        [{'#'.repeat(filledBlocks)}{'-'.repeat(emptyBlocks)}] {animatedProgress}%
      </span>
    </div>
  );
};

export default CliProgressBar;
