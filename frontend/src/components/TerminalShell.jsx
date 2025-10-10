import React from 'react';

const TerminalShell = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-950 font-mono text-green-400 overflow-hidden">
      {/* Terminal Header */}
      <div className="bg-gray-900 border-b border-green-400/30 px-4 py-2 flex justify-between items-center">
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="ml-4 text-green-400/80 text-sm tracking-wider">
            // > DIGI-FOOTPRINT ANALYZER v1.1.2
          </span>
        </div>
        <div className="flex items-center space-x-1">
          <div className="w-4 h-4 border border-green-400/50 hover:bg-green-400/20 cursor-pointer flex items-center justify-center">
            <span className="text-xs">_</span>
          </div>
          <div className="w-4 h-4 border border-green-400/50 hover:bg-green-400/20 cursor-pointer flex items-center justify-center">
            <span className="text-xs">□</span>
          </div>
          <div className="w-4 h-4 border border-green-400/50 hover:bg-green-400/20 cursor-pointer flex items-center justify-center">
            <span className="text-xs">×</span>
          </div>
        </div>
      </div>

      {/* Terminal Content Area */}
      <div className="h-[calc(100vh-60px)] overflow-y-auto p-4 bg-gray-950">
        <div className="max-w-6xl mx-auto">
          {children}
        </div>
      </div>

      {/* Terminal Footer */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-900/50 border-t border-green-400/20 px-4 py-2">
        <div className="flex justify-between items-center text-xs text-green-400/60">
          <span>STATUS: ACTIVE</span>
          <span>CONNECTION: SECURE</span>
          <span>USER: ANONYMOUS</span>
        </div>
      </div>
    </div>
  );
};

export default TerminalShell;
