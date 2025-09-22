import React, { useState, useEffect } from 'react';
import './DocumentViewer.css';

const DocumentViewer = ({ documentPath, onBack }) => {
  const [documentUrl, setDocumentUrl] = useState('');
  const [documentType, setDocumentType] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Invoice data states
  const [invoiceNumber, setInvoiceNumber] = useState('');
  const [orderNumber, setOrderNumber] = useState('');
  const [extracting, setExtracting] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [extractionError, setExtractionError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);

  useEffect(() => {
    if (documentPath) {
      // Extract file extension to determine document type
      const extension = documentPath.split('.').pop().toLowerCase();
      setDocumentType(extension);
      
      // Create document URL for serving
      // Convert path like "data/file.pdf" to "http://localhost:8000/documents/file.pdf"
      const relativePath = documentPath.replace('data/', '');
      const url = `http://localhost:8000/documents/${relativePath}`;
      setDocumentUrl(url);
      setLoading(false);
    }
    // Extract invoice data when document is loaded
    if (documentPath) {
      extractInvoiceData();
    }
  }, [documentPath]);

  const extractInvoiceData = async () => {
    setExtracting(true);
    setExtractionError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/extract-invoice-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_path: documentPath
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setInvoiceNumber(data.invoice_number || '');
        setOrderNumber(data.order_number || '');
      } else {
        setExtractionError(data.error || 'Failed to extract invoice data');
      }
    } catch (error) {
      console.error('Error extracting invoice data:', error);
      setExtractionError('Network error occurred while extracting data');
    } finally {
      setExtracting(false);
    }
  };

  const handleUpdate = async () => {
    setUpdating(true);
    
    try {
      const response = await fetch('http://localhost:8000/api/update-invoice-data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          document_path: documentPath,
          invoice_number: invoiceNumber,
          order_number: orderNumber
        })
      });
      
      const data = await response.json();
      
      if (data.success) {
        setLastUpdated(new Date().toLocaleString());
        alert('Invoice data updated successfully!');
      } else {
        alert('Failed to update invoice data: ' + (data.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error updating invoice data:', error);
      alert('Network error occurred while updating data');
    } finally {
      setUpdating(false);
    }
  };

  const handleSubmit = () => {
    // Placeholder for submit functionality - you'll implement this later
    alert('Submit functionality will be implemented later!');
  };

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
          <div className="invoice-data-panel">
            <div className="panel-header">
              <h3>📄 Invoice Data</h3>
              {extracting && <div className="extraction-status">🔄 Extracting data...</div>}
              {lastUpdated && (
                <div className="last-updated">✅ Updated: {lastUpdated}</div>
              )}
            </div>

            {extractionError && (
              <div className="extraction-error">
                <p>❌ {extractionError}</p>
                <button 
                  onClick={extractInvoiceData} 
                  className="retry-btn"
                  disabled={extracting}
                >
                  🔄 Retry Extraction
                </button>
              </div>
            )}

            <div className="invoice-fields">
              <div className="field-group">
                <label htmlFor="invoice-number">Invoice Number:</label>
                <input
                  id="invoice-number"
                  type="text"
                  value={invoiceNumber}
                  onChange={(e) => setInvoiceNumber(e.target.value)}
                  placeholder="Enter invoice number"
                  disabled={extracting}
                  className="invoice-input"
                />
              </div>

              <div className="field-group">
                <label htmlFor="order-number">Order Number:</label>
                <input
                  id="order-number"
                  type="text"
                  value={orderNumber}
                  onChange={(e) => setOrderNumber(e.target.value)}
                  placeholder="Enter order number"
                  disabled={extracting}
                  className="invoice-input"
                />
              </div>
            </div>

            <div className="action-buttons">
              <button 
                onClick={handleUpdate}
                disabled={updating || extracting}
                className="update-btn"
              >
                {updating ? '⏳ Updating...' : '📝 Update'}
              </button>
              
              <button 
                onClick={handleSubmit}
                disabled={updating || extracting || !invoiceNumber || !orderNumber}
                className="submit-btn"
              >
                ✅ Submit
              </button>
            </div>

            <div className="panel-info">
              <p className="info-text">
                💡 Data is extracted automatically using AI. You can edit the fields above and click "Update" to save changes.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentViewer;