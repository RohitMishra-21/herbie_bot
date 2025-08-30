import React, { useState, useEffect } from 'react';
import styled, { ThemeProvider, createGlobalStyle } from 'styled-components';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';

// Components
import HerbieChatInterface from './components/HerbieChatInterface';
import Header from './components/Header';
import Footer from './components/Footer';
import LoadingSpinner from './components/LoadingSpinner';

// Utils
import { apiService } from './utils/apiService';
import { soundManager } from './utils/soundManager';

// Theme
const theme = {
  colors: {
    primary: '#FF6B35',
    secondary: '#F7931E',
    accent: '#FFD23F',
    background: '#F8F9FA',
    white: '#FFFFFF',
    text: '#2C3E50',
    textLight: '#7F8C8D',
    success: '#27AE60',
    error: '#E74C3C',
    herbie: {
      blue: '#4A90E2',
      red: '#E74C3C',
      yellow: '#F1C40F',
      racing: '#2ECC71'
    }
  },
  fonts: {
    primary: "'Open Sans', sans-serif",
    heading: "'Fredoka One', cursive"
  },
  breakpoints: {
    mobile: '768px',
    tablet: '1024px',
    desktop: '1200px'
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem'
  },
  borderRadius: '8px',
  boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)'
};

// Global Styles
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #1a1a3a 100%);
    color: #E0E7FF;
    line-height: 1.6;
    overflow-x: hidden;
    min-height: 100vh;
  }

  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

  h1, h2, h3, h4, h5, h6 {
    font-family: ${props => props.theme.fonts.heading};
  }

  button {
    font-family: inherit;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  input, textarea {
    font-family: inherit;
  }

  ::-webkit-scrollbar {
    width: 8px;
  }

  ::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  ::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.primary};
    border-radius: 4px;
  }

  ::-webkit-scrollbar-thumb:hover {
    background: ${props => props.theme.colors.secondary};
  }
`;

// Styled Components
const AppContainer = styled.div`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #0a0a2e 0%, #16213e 50%, #1a1a3a 100%);
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
      radial-gradient(circle at 20% 80%, rgba(0, 162, 255, 0.1) 0%, transparent 50%),
      radial-gradient(circle at 80% 20%, rgba(0, 162, 255, 0.08) 0%, transparent 50%),
      repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0, 162, 255, 0.03) 2px,
        rgba(0, 162, 255, 0.03) 4px
      );
    opacity: 0.8;
    pointer-events: none;
  }
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
`;

const ErrorBoundary = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  padding: ${props => props.theme.spacing.xl};
  text-align: center;

  h2 {
    color: ${props => props.theme.colors.error};
    margin-bottom: ${props => props.theme.spacing.md};
  }

  p {
    color: ${props => props.theme.colors.textLight};
    margin-bottom: ${props => props.theme.spacing.lg};
  }

  button {
    background: ${props => props.theme.colors.primary};
    color: white;
    padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.lg};
    border-radius: ${props => props.theme.borderRadius};
    font-weight: 600;

    &:hover {
      background: ${props => props.theme.colors.secondary};
    }
  }
`;

// Error Boundary Component
class ErrorBoundaryComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Herbie Chatbot Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorBoundary
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <h2>🚗 Oops! Herbie hit a bump!</h2>
          <p>Something went wrong, but don't worry - Herbie is resilient!</p>
          <button onClick={() => window.location.reload()}>
            Restart Herbie
          </button>
        </ErrorBoundary>
      );
    }

    return this.props.children;
  }
}

// Main App Component
function App() {
  const [isLoading, setIsLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState('checking');
  const [error, setError] = useState(null);

  useEffect(() => {
    // Initialize app
    const initializeApp = async () => {
      try {
        // Check API health
        const health = await apiService.checkHealth();
        setApiStatus(health.status === 'healthy' ? 'connected' : 'disconnected');
        
        // Initialize sound manager
        soundManager.initialize();
        
        // Play startup sound
        soundManager.playSound('engine_start');
        
        setIsLoading(false);
      } catch (err) {
        console.error('Failed to initialize app:', err);
        setApiStatus('disconnected');
        setError('Failed to connect to Herbie. Please check your connection.');
        setIsLoading(false);
      }
    };

    // Simulate loading time for better UX
    const timer = setTimeout(initializeApp, 2000);
    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return (
      <ThemeProvider theme={theme}>
        <GlobalStyle />
        <AppContainer>
          <LoadingSpinner message="Starting up Herbie..." />
        </AppContainer>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      <ErrorBoundaryComponent>
        <Router>
          <AppContainer>
            <Header apiStatus={apiStatus} />
            <MainContent>
              <AnimatePresence mode="wait">
                <Routes>
                  <Route 
                    path="/" 
                    element={
                      <HerbieChatInterface 
                        apiStatus={apiStatus}
                        error={error}
                        onError={setError}
                      />
                    } 
                  />
                  <Route 
                    path="/chat" 
                    element={
                      <HerbieChatInterface 
                        apiStatus={apiStatus}
                        error={error}
                        onError={setError}
                      />
                    } 
                  />
                </Routes>
              </AnimatePresence>
            </MainContent>
            <Footer />
          </AppContainer>
        </Router>
      </ErrorBoundaryComponent>
    </ThemeProvider>
  );
}

export default App;