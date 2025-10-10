import React, { useState, useEffect } from 'react';
import CliSpinner from './CliSpinner';
import CliProgressBar from './CliProgressBar';

const AnalysisOutput = ({ url, onComplete, onError }) => {
  const [currentStep, setCurrentStep] = useState(0);
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const analysisSteps = [
    { text: `[TASK] Fetching profile data for ${url}...`, duration: 1000 },
    { text: `[STATUS] Establishing encrypted connection to Scraper API...`, duration: 1500, showSpinner: true },
    { text: `[PROGRESS] Data stream initiated...`, duration: 2000, showProgress: true },
    { text: `[TASK] Initiating reverse image lookup for profile_picture.jpg...`, duration: 1200 },
    { text: `[STATUS] Querying Google Custom Search API...`, duration: 1800, showSpinner: true },
    { text: `[SUCCESS] Analysis complete. Generating report...`, duration: 1000 },
  ];

  useEffect(() => {
    const performAnalysis = async () => {
      try {
        for (let i = 0; i < analysisSteps.length; i++) {
          setCurrentStep(i);
          
          if (analysisSteps[i].showProgress) {
            // Animate progress
            for (let p = 0; p <= 100; p += 10) {
              setProgress(p);
              await new Promise(resolve => setTimeout(resolve, 100));
            }
          } else {
            setProgress(0);
          }

          await new Promise(resolve => setTimeout(resolve, analysisSteps[i].duration));
        }

        // Make API call
        const response = await fetch('http://localhost:8005/platform-search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            full_name: "Test User",
            email: "test@example.com",
            platform: "twitter"
          }),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        setResult(data);
        setCurrentStep(analysisSteps.length);
        setIsComplete(true);
        
        setTimeout(() => {
          onComplete(data);
        }, 1000);

      } catch (err) {
        setError(err.message);
        setTimeout(() => {
          onError(err);
        }, 1000);
      }
    };

    performAnalysis();
  }, [url, onComplete, onError]);

  if (error) {
    return (
      <div className="space-y-2">
        {analysisSteps.slice(0, currentStep).map((step, index) => (
          <div key={index} className="text-green-400">
            {step.text}
            {step.showSpinner && index === currentStep && <CliSpinner />}
            {step.showProgress && index === currentStep && <CliProgressBar progress={progress} />}
          </div>
        ))}
        
        <div className="text-red-500">
          [ERROR] SYSTEM FAILURE: Could not retrieve data for {url}.
        </div>
        <div className="text-red-500">
          [DETAILS] {error}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {analysisSteps.map((step, index) => (
        <div key={index} className={`transition-all duration-300 ${
          index <= currentStep ? 'text-green-400' : 'text-green-400/30'
        }`}>
          {step.text}
          {step.showSpinner && index === currentStep && <CliSpinner />}
          {step.showProgress && index === currentStep && <CliProgressBar progress={progress} />}
        </div>
      ))}

      {isComplete && result && (
        <div className="mt-6 space-y-2">
          <div className="text-green-400">[RESULT] Analysis data retrieved successfully:</div>
          <div className="bg-gray-900/50 border border-green-400/30 p-4 rounded font-mono text-sm overflow-auto max-h-96">
            <pre className="text-green-300 whitespace-pre-wrap">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default AnalysisOutput;
