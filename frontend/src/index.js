import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './firebase/config'; // Initialize Firebase

// Import Google Fonts
const link = document.createElement('link');
link.href = 'https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&family=Fredoka+One:wght@400&display=swap';
link.rel = 'stylesheet';
document.head.appendChild(link);

// Get the root element
const container = document.getElementById('root');

if (!container) {
  throw new Error('Root element not found. Make sure you have a div with id="root" in your HTML.');
}

// Create root and render app
const root = createRoot(container);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Service Worker registration (optional)
if ('serviceWorker' in navigator && process.env.NODE_ENV === 'production') {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((registration) => {
        console.log('🏁 SW registered: ', registration);
      })
      .catch((registrationError) => {
        console.log('🚨 SW registration failed: ', registrationError);
      });
  });
}

// Hot Module Replacement (HMR) for development
if (module.hot) {
  module.hot.accept('./App', () => {
    const NextApp = require('./App').default;
    root.render(
      <React.StrictMode>
        <NextApp />
      </React.StrictMode>
    );
  });
}

// Performance monitoring
if (process.env.NODE_ENV === 'development') {
  import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
    getCLS(console.log);
    getFID(console.log);
    getFCP(console.log);
    getLCP(console.log);
    getTTFB(console.log);
  });
}

// Error boundary for unhandled errors
window.addEventListener('error', (event) => {
  console.error('🚨 Global error:', event.error);
});

window.addEventListener('unhandledrejection', (event) => {
  console.error('🚨 Unhandled promise rejection:', event.reason);
});

// Log app startup
console.log('🚗 Herbie Frontend Starting Up!');
console.log('🔧 Environment:', process.env.NODE_ENV);
console.log('🌐 API URL:', process.env.REACT_APP_API_URL || 'http://localhost:8000');