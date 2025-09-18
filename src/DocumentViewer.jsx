import React, { useState, useEffect } from 'react';
import './DocumentViewer.css';

const DocumentViewer = ({ documentPath, onBack }) => {
  const [documentUrl, setDocumentUrl] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (documentPath) {
      // Extract file extension to determine document type
      const extension = documentPath.split('.').pop().toLowerCase();
      setDocumentType(extension);
      
      // Create document URL for serving
      // Convert path like "data/2025-09-18/file.pdf" to "http://localhost:8000/documents/2025-09-18/file.pdf"
      const relativePath = documentPath.replace('data/', '');
      const url = `http://localhost:8000/documents/${relativePath}`;
      setDocumentUrl(url);
      setLoading(false);
    }
  }, [documentPath]);

  const renderDocument = () => {
    if (loading) {
      return (
        <div className="document-loading">
          <div className="loading-spinner"></div>
          <p>Loading document...</p>
        </div>
      );
    }

    if (error) {
      return (
        <div className="document-error">
          <h3>Error Loading Document</h3>
          <p>{error}</p>
        </div>
      );
    }

    switch (documentType) {
      case 'pdf':
        return (
          <iframe
            src={documentUrl}
            className="document-iframe"
            title="PDF Document"
            onError={() => setError('Failed to load PDF document')}
          >
            <p>Your browser doesn't support PDF viewing. <a href={documentUrl} target="_blank" rel="noopener noreferrer">Download PDF</a></p>
          </iframe>
        );
      
      case 'jpg':
      case 'jpeg':
      case 'png':
      case 'gif':
        return (
          <div className="document-image-container">
            <img
              src={documentUrl}
              alt="Document"
              className="document-image"
              onError={() => setError('Failed to load image document')}
            />
          </div>
        );
      
      case 'txt':
      case 'csv':
        return (
          <iframe
            src={documentUrl}
            className="document-iframe"
            title="Text Document"
            onError={() => setError('Failed to load text document')}
          >
            <p>Your browser doesn't support viewing this file type. <a href={documentUrl} target="_blank" rel="noopener noreferrer">Download file</a></p>
          </iframe>
        );
      
      default:
        return (
          <div className="document-unsupported">
            <h3>Unsupported Document Type</h3>
            <p>File type: {documentType.toUpperCase()}</p>
            <p>The document cannot be displayed in the browser.</p>
            <a 
              href={documentUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="download-link"
            >
              Download Document
            </a>
          </div>
        );
    }
  };

  return (
    <div className="document-viewer">
      <div className="document-header">
        <button onClick={onBack} className="back-button">
          ← Back to Processing
        </button>
        <div className="document-info">
          <h1>Document Viewer</h1>
          <p className="document-name">
            {documentPath ? documentPath.split('/').pop() : 'Loading...'}
          </p>
        </div>
      </div>

      <div className="document-content">
        <div className="document-left-panel">
          <div className="document-container">
            <div className="document-toolbar">
              <span className="document-type-badge">
                {documentType.toUpperCase()}
              </span>
              <a 
                href={documentUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="external-link-btn"
                title="Open in new tab"
              >
                🔗 Open External
              </a>
            </div>
            {renderDocument()}
          </div>
        </div>

        <div className="document-right-panel">
          <div className="right-panel-placeholder">
            <div className="placeholder-content">
              <h3>Analysis Panel</h3>
              <p>This panel will be used for document analysis and processing.</p>
              <div className="placeholder-features">
                <div className="feature-item">📊 Document Analysis</div>
                <div className="feature-item">🤖 AI Processing</div>
                <div className="feature-item">📝 Text Extraction</div>
                <div className="feature-item">🔍 Content Search</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;