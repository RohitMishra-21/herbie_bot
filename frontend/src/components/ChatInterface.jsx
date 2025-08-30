import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { apiService } from '../utils/apiService';
import { soundManager } from '../utils/soundManager';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);
  max-width: 1000px;
  margin: 0 auto;
  padding: ${props => props.theme.spacing.lg};
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: ${props => props.theme.borderRadius};
  box-shadow: ${props => props.theme.boxShadow};
  border: 1px solid rgba(255, 255, 255, 0.2);

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    height: calc(100vh - 150px);
    padding: ${props => props.theme.spacing.md};
  }
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${props => props.theme.spacing.md};
  margin-bottom: ${props => props.theme.spacing.lg};
  display: flex;
  flex-direction: column;
  gap: ${props => props.theme.spacing.md};

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.primary};
    border-radius: 3px;
  }
`;

const MessageBubble = styled(motion.div)`
  max-width: 70%;
  padding: ${props => props.theme.spacing.md};
  border-radius: 20px;
  word-wrap: break-word;
  position: relative;
  
  ${props => props.isUser ? `
    align-self: flex-end;
    background: linear-gradient(135deg, ${props.theme.colors.primary}, ${props.theme.colors.secondary});
    color: white;
    border-bottom-right-radius: 8px;
  ` : `
    align-self: flex-start;
    background: rgba(255, 255, 255, 0.9);
    color: ${props.theme.colors.text};
    border-bottom-left-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.3);
  `}

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    max-width: 85%;
  }
`;

const EmotionBadge = styled.span`
  display: inline-block;
  background: ${props => props.theme.colors.accent};
  color: ${props => props.theme.colors.text};
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-top: ${props => props.theme.spacing.xs};
  opacity: 0.8;
`;

const InputContainer = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  align-items: flex-end;
`;

const MessageInput = styled.textarea`
  flex: 1;
  padding: ${props => props.theme.spacing.md};
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  color: white;
  font-size: 1rem;
  line-height: 1.4;
  resize: none;
  min-height: 50px;
  max-height: 120px;
  transition: all 0.3s ease;

  &::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }

  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    background: rgba(255, 255, 255, 0.15);
  }
`;

const SendButton = styled(motion.button)`
  background: linear-gradient(135deg, ${props => props.theme.colors.primary}, ${props => props.theme.colors.secondary});
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  padding: ${props => props.theme.spacing.md};
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  align-self: flex-start;
  max-width: 150px;

  .dot {
    width: 8px;
    height: 8px;
    background: ${props => props.theme.colors.primary};
    border-radius: 50%;
  }
`;

const ErrorMessage = styled(motion.div)`
  background: ${props => props.theme.colors.error};
  color: white;
  padding: ${props => props.theme.spacing.md};
  border-radius: ${props => props.theme.borderRadius};
  margin-bottom: ${props => props.theme.spacing.md};
  text-align: center;
`;

const WelcomeMessage = styled(motion.div)`
  text-align: center;
  padding: ${props => props.theme.spacing.xl};
  color: white;

  h2 {
    font-size: 2rem;
    margin-bottom: ${props => props.theme.spacing.md};
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  }

  p {
    font-size: 1.1rem;
    opacity: 0.9;
    line-height: 1.6;
  }
`;

function ChatInterface({ apiStatus, error, onError }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    // Welcome message
    if (apiStatus === 'connected' && messages.length === 0) {
      setMessages([{
        id: Date.now(),
        text: "🤖 Greetings! I am H.E.R.B.I.E. - Humanoid Experimental Robot, B-type, Integrated Electronics! I am online and ready to assist the Fantastic Four!",
        isUser: false,
        emotion: 'friendly',
        timestamp: new Date()
      }]);
    }
  }, [apiStatus, messages.length]);

  const handleSendMessage = async () => {
    if (!input.trim() || isSending || apiStatus !== 'connected') return;

    const userMessage = {
      id: Date.now(),
      text: input.trim(),
      isUser: true,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsSending(true);
    setIsTyping(true);

    try {
      soundManager.playSound('message_send');
      
      const response = await apiService.sendMessage(input.trim());
      
      setTimeout(() => {
        const herbieMessage = {
          id: Date.now() + 1,
          text: response.response,
          isUser: false,
          emotion: response.emotion,
          confidence: response.confidence,
          timestamp: new Date()
        };

        setMessages(prev => [...prev, herbieMessage]);
        setIsTyping(false);
        soundManager.playSound('message_receive');
        
        if (onError) onError(null);
      }, 1000 + Math.random() * 1000); // Simulate thinking time

    } catch (err) {
      console.error('Chat error:', err);
      setIsTyping(false);
      
      const errorMessage = {
        id: Date.now() + 1,
        text: "🔧 Oops! Herbie's circuits got a bit tangled. Could you try that again?",
        isUser: false,
        emotion: 'confused',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
      
      if (onError) {
        onError('Failed to get response from Herbie. Please try again.');
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
    }
  };

  const typingVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: { opacity: 1, y: 0 }
  };

  if (apiStatus === 'checking') {
    return (
      <ChatContainer>
        <WelcomeMessage
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <h2>🤖 Starting H.E.R.B.I.E...</h2>
          <p>Connecting to H.E.R.B.I.E. - Fantastic Four's AI Assistant!</p>
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
          <p>Cannot connect to H.E.R.B.I.E. systems. Please check that the backend is running on port 8000.</p>
        </WelcomeMessage>
      </ChatContainer>
    );
  }

  return (
    <ChatContainer>
      {error && (
        <ErrorMessage
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
        >
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
              exit="hidden"
            >
              {message.text}
              {!message.isUser && message.emotion && (
                <EmotionBadge>{message.emotion}</EmotionBadge>
              )}
            </MessageBubble>
          ))}

          {isTyping && (
            <TypingIndicator
              variants={typingVariants}
              initial="hidden"
              animate="visible"
              exit="hidden"
            >
              <span>Herbie is thinking</span>
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
          placeholder="Ask Herbie anything... 🏁"
          disabled={isSending || apiStatus !== 'connected'}
          rows={1}
        />
        <SendButton
          onClick={handleSendMessage}
          disabled={!input.trim() || isSending || apiStatus !== 'connected'}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          🚀
        </SendButton>
      </InputContainer>
    </ChatContainer>
  );
}

export default ChatInterface;