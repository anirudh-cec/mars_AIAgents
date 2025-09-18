import React from 'react';
import { createRoot } from 'react-dom/client';
import ProcessingPage from './ProcessingPage';

// Get the root element
const container = document.getElementById('root');
const root = createRoot(container);

// Render the ProcessingPage component
root.render(
  <React.StrictMode>
    <ProcessingPage />
  </React.StrictMode>
);