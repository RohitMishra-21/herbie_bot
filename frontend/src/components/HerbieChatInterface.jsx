import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes } from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
// Removed anime.js - using CSS animations and framer-motion instead
import { apiService } from '../utils/apiService';
import { soundManager } from '../utils/soundManager';

// Sci-fi animations
const pulseGlow = keyframes`
  0% { box-shadow: 0 0 20px rgba(0, 162, 255, 0.5); }
  50% { box-shadow: 0 0 40px rgba(0, 162, 255, 0.8), 0 0 60px rgba(0, 162, 255, 0.4); }
  100% { box-shadow: 0 0 20px rgba(0, 162, 255, 0.5); }
`;

const scanLine = keyframes`
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100vw); }
`;

const dataFlow = keyframes`
  0% { transform: translateY(100%); opacity: 0; }
  50% { opacity: 1; }
  100% { transform: translateY(-100%); opacity: 0; }
`;

const avatarSpin = keyframes`
  0% { transform: rotateY(0deg) scale(1); }
  50% { transform: rotateY(180deg) scale(1.1); }
  100% { transform: rotateY(360deg) scale(1); }
`;

// Main container with sci-fi styling
const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: 
    linear-gradient(135deg, 
      rgba(0, 10, 30, 0.85) 0%,
      rgba(0, 25, 50, 0.8) 50%,
      rgba(0, 40, 80, 0.85) 100%
    ),
    url('/images/herbie/backgrounds/fantastic-four-space.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 2px solid rgba(0, 162, 255, 0.3);
  box-shadow: 
    0 0 50px rgba(0, 162, 255, 0.2),
    inset 0 0 50px rgba(0, 162, 255, 0.05);
  position: relative;
  overflow: hidden;

  /* Global animation for avatar spin */
  .avatar-container {
    &.spinning {
      animation: ${avatarSpin} 0.8s ease-in-out;
    }
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(0, 162, 255, 0.8), transparent);
    animation: ${scanLine} 3s linear infinite;
    z-index: 1;
  }

  @media (max-width: 768px) {
    height: calc(100vh - 80px);
    padding: 15px;
  }
`;

// Header with HERBIE branding
const HerbieHeader = styled.div`
  text-align: center;
  padding: 20px;
  margin-bottom: 20px;
  border-bottom: 1px solid rgba(0, 162, 255, 0.3);
  position: relative;

  h1 {
    font-family: 'Orbitron', 'Courier New', monospace;
    font-size: 2.5rem;
    font-weight: 900;
    color: #00A2FF;
    text-shadow: 
      0 0 10px rgba(0, 162, 255, 0.8),
      0 0 20px rgba(0, 162, 255, 0.6),
      0 0 30px rgba(0, 162, 255, 0.4);
    margin: 0;
    letter-spacing: 3px;
    animation: ${pulseGlow} 2s ease-in-out infinite;
  }

  .subtitle {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: rgba(0, 162, 255, 0.8);
    margin-top: 5px;
    letter-spacing: 1px;
    text-transform: uppercase;
  }

  .avatar-container {
    width: 80px;
    height: 80px;
    margin: 15px auto;
    border-radius: 50%;
    border: 3px solid rgba(0, 162, 255, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    background: radial-gradient(circle, rgba(0, 162, 255, 0.2), rgba(0, 40, 80, 0.8));
    animation: ${pulseGlow} 3s ease-in-out infinite;
    cursor: pointer;
    transition: all 0.3s ease;
    overflow: hidden;

    &:hover {
      transform: scale(1.1);
      border-color: rgba(0, 162, 255, 0.8);
    }

    .herbie-avatar {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
      filter: drop-shadow(0 0 10px rgba(0, 162, 255, 0.6));
    }

    .robot-icon {
      font-size: 2.5rem;
      color: #00A2FF;
      text-shadow: 0 0 10px rgba(0, 162, 255, 0.8);
    }
  }
`;

// Status indicator
const StatusIndicator = styled.div`
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  background: rgba(0, 162, 255, 0.1);
  border: 1px solid rgba(0, 162, 255, 0.3);
  border-radius: 20px;
  margin-bottom: 20px;
  font-family: 'Rajdhani', sans-serif;
  color: #00A2FF;

  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: ${props => props.connected ? '#00FF88' : '#FF4444'};
    animation: ${pulseGlow} 1s ease-in-out infinite;
  }
`;

// Messages container with sci-fi styling
const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    width: 2px;
    height: 100%;
    background: linear-gradient(to bottom, 
      transparent, 
      rgba(0, 162, 255, 0.3), 
      rgba(0, 162, 255, 0.6), 
      rgba(0, 162, 255, 0.3), 
      transparent
    );
    animation: ${dataFlow} 2s linear infinite;
  }

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(0, 162, 255, 0.1);
    border-radius: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: rgba(0, 162, 255, 0.5);
    border-radius: 4px;
    border: 1px solid rgba(0, 162, 255, 0.3);
  }
`;

// Message bubbles with different styles for user vs HERBIE
const MessageBubble = styled(motion.div)`
  max-width: 80%;
  padding: 18px 24px;
  border-radius: 20px;
  position: relative;
  font-family: 'Inter', sans-serif;
  line-height: 1.5;
  
  ${props => props.isUser ? `
    align-self: flex-end;
    background: linear-gradient(135deg, 
      rgba(0, 162, 255, 0.8) 0%,
      rgba(0, 100, 200, 0.9) 100%
    );
    color: white;
    border-bottom-right-radius: 8px;
    border: 1px solid rgba(0, 162, 255, 0.6);
    box-shadow: 0 8px 32px rgba(0, 162, 255, 0.2);

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      right: -8px;
      width: 0;
      height: 0;
      border: 8px solid transparent;
      border-top-color: rgba(0, 100, 200, 0.9);
    }
  ` : `
    align-self: flex-start;
    background: linear-gradient(135deg,
      rgba(20, 20, 40, 0.9) 0%,
      rgba(30, 30, 60, 0.95) 100%
    );
    color: #E0E7FF;
    border-bottom-left-radius: 8px;
    border: 1px solid rgba(0, 162, 255, 0.4);
    box-shadow: 
      0 8px 32px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(0, 162, 255, 0.2);

    &::after {
      content: '';
      position: absolute;
      bottom: 0;
      left: -8px;
      width: 0;
      height: 0;
      border: 8px solid transparent;
      border-top-color: rgba(30, 30, 60, 0.95);
    }
  `}

  .message-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    opacity: 0.8;
    
    .sender-name {
      font-weight: 600;
      color: ${props => props.isUser ? 'rgba(255,255,255,0.9)' : '#00A2FF'};
    }
    
    .timestamp {
      font-family: 'Courier New', monospace;
      font-size: 0.7rem;
      opacity: 0.6;
    }
  }

  @media (max-width: 768px) {
    max-width: 90%;
    padding: 15px 18px;
  }
`;

// Emotion badge with sci-fi styling
const EmotionBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: rgba(0, 162, 255, 0.2);
  color: #00A2FF;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
  font-family: 'Rajdhani', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-top: 8px;
  border: 1px solid rgba(0, 162, 255, 0.3);
  
  .emotion-icon {
    font-size: 0.8rem;
  }
`;

// Typing indicator with advanced animation
const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px 20px;
  background: rgba(20, 20, 40, 0.9);
  border: 1px solid rgba(0, 162, 255, 0.4);
  border-radius: 20px;
  align-self: flex-start;
  max-width: 200px;
  font-family: 'Rajdhani', sans-serif;
  color: #00A2FF;
  font-weight: 500;

  .typing-text {
    font-size: 0.9rem;
  }

  .dots-container {
    display: flex;
    gap: 4px;
  }

  .dot {
    width: 6px;
    height: 6px;
    background: #00A2FF;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(0, 162, 255, 0.6);
  }
`;

// Input area with futuristic design
const InputContainer = styled.div`
  display: flex;
  gap: 15px;
  align-items: flex-end;
  padding: 20px;
  background: rgba(0, 10, 30, 0.8);
  border-top: 1px solid rgba(0, 162, 255, 0.3);
  border-radius: 0 0 18px 18px;
`;

const MessageInput = styled.textarea`
  flex: 1;
  padding: 15px 20px;
  border: 2px solid rgba(0, 162, 255, 0.4);
  border-radius: 25px;
  background: rgba(0, 20, 40, 0.8);
  backdrop-filter: blur(10px);
  color: #E0E7FF;
  font-size: 1rem;
  font-family: 'Inter', sans-serif;
  line-height: 1.4;
  resize: none;
  min-height: 50px;
  max-height: 120px;
  transition: all 0.3s ease;

  &::placeholder {
    color: rgba(0, 162, 255, 0.6);
    font-style: italic;
  }

  &:focus {
    outline: none;
    border-color: #00A2FF;
    background: rgba(0, 30, 60, 0.9);
    box-shadow: 
      0 0 20px rgba(0, 162, 255, 0.3),
      inset 0 0 20px rgba(0, 162, 255, 0.1);
  }
`;

const SendButton = styled(motion.button)`
  background: linear-gradient(135deg, #00A2FF, #0080CC);
  color: white;
  border: none;
  border-radius: 50%;
  width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid rgba(0, 162, 255, 0.6);
  box-shadow: 0 4px 20px rgba(0, 162, 255, 0.3);

  &:hover:not(:disabled) {
    background: linear-gradient(135deg, #00B8FF, #0099DD);
    box-shadow: 0 6px 30px rgba(0, 162, 255, 0.5);
    border-color: #00A2FF;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background: rgba(0, 162, 255, 0.3);
  }

  .send-icon {
    transition: transform 0.3s ease;
  }

  &:hover:not(:disabled) .send-icon {
    transform: translateX(2px);
  }
`;

// Welcome screen with HERBIE intro
const WelcomeMessage = styled(motion.div)`
  text-align: center;
  padding: 40px 20px;
  color: #E0E7FF;

  h2 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2rem;
    margin-bottom: 20px;
    color: #00A2FF;
    text-shadow: 0 0 20px rgba(0, 162, 255, 0.6);
  }

  p {
    font-size: 1.1rem;
    opacity: 0.9;
    line-height: 1.6;
    max-width: 600px;
    margin: 0 auto 20px;
  }

  .features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-top: 30px;

    .feature {
      padding: 15px;
      background: rgba(0, 162, 255, 0.1);
      border: 1px solid rgba(0, 162, 255, 0.3);
      border-radius: 12px;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(0, 162, 255, 0.15);
        transform: translateY(-2px);
      }

      .feature-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
        color: #00A2FF;
      }

      .feature-title {
        font-weight: 600;
        margin-bottom: 5px;
        color: #00A2FF;
      }

      .feature-desc {
        font-size: 0.9rem;
        opacity: 0.8;
      }
    }
  }
`;

// Error message component
const ErrorMessage = styled(motion.div)`
  background: linear-gradient(135deg, rgba(255, 68, 68, 0.9), rgba(200, 30, 30, 0.9));
  color: white;
  padding: 15px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  text-align: center;
  border: 1px solid rgba(255, 68, 68, 0.5);
  box-shadow: 0 4px 20px rgba(255, 68, 68, 0.2);
  
  .error-icon {
    margin-right: 8px;
    font-size: 1.1rem;
  }
`;

// Emotion icons mapping
const emotionIcons = {
  friendly: '😊',
  helpful: '🤝',
  urgent: '⚠️',
  concerned: '😟',
  thoughtful: '🤔',
  neutral: '🤖',
  confused: '😕'
};

function HerbieChatInterface({ apiStatus, error, onError }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [currentEmotion, setCurrentEmotion] = useState('neutral');
  const messagesEndRef = useRef(null);
  const avatarRef = useRef(null);

  // Function to get avatar image based on emotion
  const getAvatarImage = (emotion = 'neutral') => {
    const avatarMap = {
      friendly: '/images/herbie/avatars/herbie-happy.png',
      helpful: '/images/herbie/avatars/herbie-happy.png',
      urgent: '/images/herbie/avatars/herbie-alert.png',
      concerned: '/images/herbie/avatars/herbie-alert.png',
      thoughtful: '/images/herbie/avatars/herbie-thinking.png',
      confused: '/images/herbie/avatars/herbie-thinking.png',
      neutral: '/images/herbie/avatars/herbie-main-avatar.png'
    };
    return avatarMap[emotion] || avatarMap.neutral;
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  // Initialize with HERBIE welcome message
  useEffect(() => {
    if (apiStatus === 'connected' && messages.length === 0) {
      setMessages([{
        id: Date.now(),
        text: "Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics. I am online and ready to assist the Fantastic Four! How may I help you today?",
        isUser: false,
        emotion: 'friendly',
        timestamp: new Date(),
        sender: 'H.E.R.B.I.E.'
      }]);
    }
  }, [apiStatus, messages.length]);

  // Avatar click animation using CSS classes
  const handleAvatarClick = () => {
    if (avatarRef.current) {
      avatarRef.current.classList.remove('spinning');
      void avatarRef.current.offsetHeight; // Trigger reflow
      avatarRef.current.classList.add('spinning');
      setTimeout(() => {
        if (avatarRef.current) {
          avatarRef.current.classList.remove('spinning');
        }
      }, 800);
    }
  };

  const handleSendMessage = async () => {
    if (!input.trim() || isSending || apiStatus !== 'connected') return;

    const userMessage = {
      id: Date.now(),
      text: input.trim(),
      isUser: true,
      timestamp: new Date(),
      sender: 'User'
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsSending(true);
    setIsTyping(true);

    try {
      soundManager.playSound('message_send');
      
      const response = await apiService.sendMessage(input.trim());
      
      // Simulate HERBIE processing time
      setTimeout(() => {
        const herbieMessage = {
          id: Date.now() + 1,
          text: response.response,
          isUser: false,
          emotion: response.emotion,
          confidence: response.confidence,
          timestamp: new Date(),
          sender: 'H.E.R.B.I.E.'
        };

        setMessages(prev => [...prev, herbieMessage]);
        setCurrentEmotion(response.emotion || 'neutral');
        setIsTyping(false);
        soundManager.playSound('message_receive');
        
        if (onError) onError(null);
      }, 800 + Math.random() * 1200);

    } catch (err) {
      console.error('Chat error:', err);
      setIsTyping(false);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "Alert! My circuits are experiencing interference. Please try your query again.",
        isUser: false,
        emotion: 'confused',
        timestamp: new Date(),
        sender: 'H.E.R.B.I.E.'
      };

      setMessages(prev => [...prev, errorMessage]);
      
      if (onError) {
        onError('Connection error with H.E.R.B.I.E. Please try again.');
      }
    } finally {
      setIsSending(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Animation variants
  const messageVariants = {
    hidden: { opacity: 0, y: 20, scale: 0.8 },
    visible: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { 
        type: "spring",
        stiffness: 500,
        damping: 30
      }
    },
    exit: { opacity: 0, scale: 0.8, transition: { duration: 0.2 } }
  };

  const typingVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 },
    exit: { opacity: 0, y: -10 }
  };

  if (apiStatus === 'checking') {
    return (
      <ChatContainer>
        <WelcomeMessage
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2>🤖 Initializing H.E.R.B.I.E...</h2>
          <p>Connecting to Humanoid Experimental Robot, B-type, Integrated Electronics</p>
          <div className="features">
            <div className="feature">
              <div className="feature-icon">⚡</div>
              <div className="feature-title">Instant Analysis</div>
              <div className="feature-desc">Real-time data processing</div>
            </div>
            <div className="feature">
              <div className="feature-icon">🛡️</div>
              <div className="feature-title">Team Protection</div>
              <div className="feature-desc">Fantastic Four support</div>
            </div>
            <div className="feature">
              <div className="feature-icon">🧠</div>
              <div className="feature-title">Advanced AI</div>
              <div className="feature-desc">Intelligent assistance</div>
            </div>
          </div>
        </WelcomeMessage>
      </ChatContainer>
    );
  }

  if (apiStatus === 'disconnected') {
    return (
      <ChatContainer>
        <WelcomeMessage
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2>🔧 H.E.R.B.I.E. Offline</h2>
          <p>Cannot establish connection to H.E.R.B.I.E. systems. Please check that the backend server is running on port 8000.</p>
        </WelcomeMessage>
      </ChatContainer>
    );
  }

  return (
    <ChatContainer>
      <HerbieHeader>
        <div className="avatar-container" ref={avatarRef} onClick={handleAvatarClick}>
          {/* Try to load HERBIE avatar image, fallback to robot icon */}
          <img 
            src={getAvatarImage(currentEmotion)}
            alt={`H.E.R.B.I.E. Avatar - ${currentEmotion}`}
            className="herbie-avatar"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextElementSibling.style.display = 'block';
            }}
          />
          <div className="robot-icon" style={{display: 'none'}}>🤖</div>
        </div>
        <h1>H.E.R.B.I.E.</h1>
        <div className="subtitle">Humanoid Experimental Robot, B-type, Integrated Electronics</div>
      </HerbieHeader>

      <StatusIndicator connected={apiStatus === 'connected'}>
        <div className="status-dot"></div>
        <span>
          {apiStatus === 'connected' ? 'Systems Online' : 'Systems Offline'}
        </span>
      </StatusIndicator>

      {error && (
        <ErrorMessage
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
          <span className="error-icon">⚠️</span>
          {error}
        </ErrorMessage>
      )}

      <MessagesContainer>
        <AnimatePresence>
          {messages.map((message) => (
            <MessageBubble
              key={message.id}
              isUser={message.isUser}
              variants={messageVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              <div className="message-header">
                <span className="sender-name">{message.sender}</span>
                <span className="timestamp">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
              {message.text}
              {!message.isUser && message.emotion && (
                <EmotionBadge>
                  <span className="emotion-icon">
                    {emotionIcons[message.emotion] || '🤖'}
                  </span>
                  {message.emotion}
                </EmotionBadge>
              )}
            </MessageBubble>
          ))}

          {isTyping && (
            <TypingIndicator
              variants={typingVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              <span className="typing-text">H.E.R.B.I.E. is analyzing</span>
              <div className="dots-container">
                <motion.div
                  className="dot"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 0.6, delay: 0 }}
                />
                <motion.div
                  className="dot"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }}
                />
                <motion.div
                  className="dot"
                  animate={{ scale: [1, 1.2, 1] }}
                  transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }}
                />
              </div>
            </TypingIndicator>
          )}
        </AnimatePresence>
        <div ref={messagesEndRef} />
      </MessagesContainer>

      <InputContainer>
        <MessageInput
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Communicate with H.E.R.B.I.E..."
          disabled={isSending || apiStatus !== 'connected'}
          rows={1}
        />
        <SendButton
          onClick={handleSendMessage}
          disabled={!input.trim() || isSending || apiStatus !== 'connected'}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <span className="send-icon">⚡</span>
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
}

export default HerbieChatInterface;