import React, { useState } from 'react';
import './ProcessingPage.css';
import DocumentViewer from './DocumentViewer';

const ProcessingPage = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showDocumentViewer, setShowDocumentViewer] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState(null);

  const handleStartProcessing = async () => {
    setIsProcessing(true);
    setError(null);
    setResult(null);
    
    try {
      console.log('Starting Gmail processing...');
      
      // Call FastAPI backend
      const response = await fetch('http://localhost:8000/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action: 'start_processing'
        })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Processing result:', data);
      
      setResult(data);
      
      // Auto-navigate to document viewer if files were downloaded successfully
      if (data.success && data.files_downloaded && data.files_downloaded.length > 0) {
        // Show the first downloaded file (you can modify this to show a selection if multiple files)
        const firstFile = data.files_downloaded[0];
        setSelectedDocument(firstFile);
        
        // Delay navigation to show success message briefly
        setTimeout(() => {
          setShowDocumentViewer(true);
        }, 2000);
      }
      
    } catch (err) {
      console.error('Error during processing:', err);
      setError(err.message || 'An error occurred during processing');
    } finally {
      setIsProcessing(false);
    }
  };
  
  const handleBackToProcessing = () => {
    setShowDocumentViewer(false);
    setSelectedDocument(null);
    // Optionally clear previous results
    setResult(null);
    setError(null);
  };
  
  const handleViewDocument = (documentPath) => {
    setSelectedDocument(documentPath);
    setShowDocumentViewer(true);
  };

  // Show DocumentViewer if a document is selected
  if (showDocumentViewer && selectedDocument) {
    return (
      <DocumentViewer 
        documentPath={selectedDocument}
        onBack={handleBackToProcessing}
      />
    );
  }

  // Show main processing page
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
                
                {/* Result Display Section */}
                {(result || error) && (
                  <div className="result-section">
                    {error && (
                      <div className="error-message">
                        <h3>Error</h3>
                        <p>{error}</p>
                      </div>
                    )}
                    
                    {result && (
                      <div className={`result-message ${result.success ? 'success' : 'info'}`}>
                        <h3>Processing Results</h3>
                        <p className="main-message">{result.message}</p>
                        
                        {result.success && result.files_downloaded && result.files_downloaded.length > 0 && (
                          <div className="files-info">
                            <h4>Downloaded Files ({result.files_downloaded.length}):</h4>
                            <ul className="files-list">
                              {result.files_downloaded.map((file, index) => (
                                <li key={index} className="file-item">
                                  <div className="file-info">
                                    <span className="file-name">{file.split('/').pop()}</span>
                                    <span className="file-path">{file}</span>
                                  </div>
                                  <button 
                                    className="view-document-btn"
                                    onClick={() => handleViewDocument(file)}
                                    title="View Document"
                                  >
                                    👁️ View
                                  </button>
                                </li>
                              ))}
                            </ul>
                            <p className="emails-processed">
                              Processed {result.emails_processed} email{result.emails_processed !== 1 ? 's' : ''}
                            </p>
                          </div>
                        )}
                        
                        {!result.success && result.message === 'No new records to display' && (
                          <div className="no-records">
                            <p>✉️ No new emails with attachments found from demotest.tcs@gmail.com</p>
                          </div>
                        )}
                        
                        <p className="timestamp">
                          {new Date(result.timestamp).toLocaleString()}
                        </p>
                      </div>
                    )}
                  </div>
                )}
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
