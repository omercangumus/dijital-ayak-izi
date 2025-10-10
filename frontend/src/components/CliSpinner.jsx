import React, { useState, useEffect } from 'react';

const CliSpinner = ({ text = "Loading" }) => {
  const [spinnerIndex, setSpinnerIndex] = useState(0);
  const spinners = ['|', '/', '-', '\\'];

  useEffect(() => {
    const interval = setInterval(() => {
      setSpinnerIndex((prev) => (prev + 1) % spinners.length);
    }, 100);

    return () => clearInterval(interval);
  }, []);

  return (
    <span className="inline-flex items-center space-x-2">
      <span className="text-green-400">{text}</span>
      <span className="text-green-400 font-mono">[{spinners[spinnerIndex]}]</span>
    </span>
  );
};

export default CliSpinner;
