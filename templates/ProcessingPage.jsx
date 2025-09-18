import React, { useState } from 'react';
import '../static/ProcessingPage.css';

const ProcessingPage = () => {
  const [isProcessing, setIsProcessing] = useState(false);

  const handleStartProcessing = () => {
    setIsProcessing(true);
    // Functionality will be defined later
    console.log('Start Processing button clicked');
    
    // Reset processing state after animation (optional)
    setTimeout(() => {
      setIsProcessing(false);
    }, 2000);
  };

  return (
    <div className="processing-page">
      <div className="background-overlay"></div>
      
      <div className="content-container">
        <header className="page-header">
          <h1 className="main-title">Mars AI Agents</h1>
          <p className="subtitle">Advanced Processing System</p>
        </header>

        <main className="main-content">
          <div className="processing-section">
            <div className="processing-card">
              <div className="card-content">
                <h2 className="processing-title">Ready to Begin</h2>
                <p className="processing-description">
                  Initialize the AI processing system to start your Mars exploration journey.
                </p>
                
                <button 
                  className={`start-button ${isProcessing ? 'processing' : ''}`}
                  onClick={handleStartProcessing}
                  disabled={isProcessing}
                >
                  <span className="button-text">
                    {isProcessing ? 'Processing...' : 'Start Processing'}
                  </span>
                  <div className="button-ripple"></div>
                </button>
              </div>
            </div>
          </div>
        </main>

        <footer className="page-footer">
          <p>&copy; 2025 Mars AI Agents. All Rights Reserved.</p>
        </footer>
      </div>
    </div>
  );
};

export default ProcessingPage;