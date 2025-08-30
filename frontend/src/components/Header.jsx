import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const HeaderContainer = styled.header`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  padding: ${props => props.theme.spacing.lg} ${props => props.theme.spacing.xl};
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
    animation: shine 3s infinite;
  }

  @keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    padding: ${props => props.theme.spacing.md};
  }
`;

const HeaderContent = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 1;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.md};
    text-align: center;
  }
`;

const Logo = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.md};

  h1 {
    font-family: ${props => props.theme.fonts.heading};
    font-size: 2.5rem;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    margin: 0;
    letter-spacing: 2px;

    @media (max-width: ${props => props.theme.breakpoints.mobile}) {
      font-size: 2rem;
    }
  }

  .logo-icon {
    font-size: 3rem;
    filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));

    @media (max-width: ${props => props.theme.breakpoints.mobile}) {
      font-size: 2.5rem;
    }
  }
`;

const Subtitle = styled.p`
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
  margin: ${props => props.theme.spacing.xs} 0 0 0;
  font-weight: 300;
  letter-spacing: 1px;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    font-size: 0.9rem;
  }
`;

const StatusSection = styled.div`
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: ${props => props.theme.spacing.sm};

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    align-items: center;
  }
`;

const StatusIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 0.9rem;
  font-weight: 500;
`;

const StatusDot = styled.div`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: ${props => {
    switch (props.status) {
      case 'connected': return props.theme.colors.success;
      case 'disconnected': return props.theme.colors.error;
      case 'checking': return props.theme.colors.herbie.yellow;
      default: return props.theme.colors.textLight;
    }
  }};
  animation: ${props => props.status === 'checking' ? 'pulse 1.5s infinite' : 'none'};

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
  }
`;

const StatusText = styled.span`
  color: white;
  font-weight: 600;
`;

const VersionBadge = styled.div`
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.5px;
`;

const RacingStripe = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, 
    ${props => props.theme.colors.herbie.red} 0%, 
    ${props => props.theme.colors.herbie.blue} 50%, 
    ${props => props.theme.colors.herbie.red} 100%
  );
`;

function Header({ apiStatus = 'checking' }) {
  const getStatusText = (status) => {
    switch (status) {
      case 'connected': return 'Online & Ready';
      case 'disconnected': return 'Offline';
      case 'checking': return 'Connecting...';
      default: return 'Unknown';
    }
  };

  const logoVariants = {
    initial: { opacity: 0, y: -20 },
    animate: { 
      opacity: 1, 
      y: 0,
      transition: { 
        duration: 0.8,
        ease: "easeOut"
      }
    }
  };

  const statusVariants = {
    initial: { opacity: 0, x: 20 },
    animate: { 
      opacity: 1, 
      x: 0,
      transition: { 
        duration: 0.8,
        delay: 0.3,
        ease: "easeOut"
      }
    }
  };

  return (
    <HeaderContainer>
      <RacingStripe />
      <HeaderContent>
        <Logo
          variants={logoVariants}
          initial="initial"
          animate="animate"
        >
          <motion.div 
            className="logo-icon"
            animate={{ 
              rotate: [0, 5, -5, 0],
            }}
            transition={{ 
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            🤖
          </motion.div>
          <div>
            <h1>H.E.R.B.I.E.</h1>
            <Subtitle>
              Humanoid Experimental Robot, B-type, Integrated Electronics
            </Subtitle>
          </div>
        </Logo>

        <StatusSection>
          <StatusIndicator
            variants={statusVariants}
            initial="initial"
            animate="animate"
          >
            <StatusDot status={apiStatus} />
            <StatusText>{getStatusText(apiStatus)}</StatusText>
          </StatusIndicator>
          <VersionBadge>v1.0.0</VersionBadge>
        </StatusSection>
      </HeaderContent>
    </HeaderContainer>
  );
}

export default Header;