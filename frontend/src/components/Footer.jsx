import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const FooterContainer = styled.footer`
  background: rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: ${props => props.theme.spacing.lg} ${props => props.theme.spacing.xl};
  position: relative;
  overflow: hidden;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    padding: ${props => props.theme.spacing.md};
  }
`;

const FooterContent = styled.div`
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

const FooterText = styled.div`
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.sm};

  .heart {
    color: ${props => props.theme.colors.error};
    animation: heartbeat 2s infinite;
  }

  @keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.xs};
  }
`;

const RacingInfo = styled.div`
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.md};
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    flex-direction: column;
    gap: ${props => props.theme.spacing.xs};
  }
`;

const RacingBadge = styled(motion.div)`
  background: linear-gradient(45deg, ${props => props.theme.colors.herbie.racing}, ${props => props.theme.colors.success});
  color: white;
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: 15px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  box-shadow: 0 2px 8px rgba(46, 204, 113, 0.3);
`;

const SocialLinks = styled.div`
  display: flex;
  gap: ${props => props.theme.spacing.md};
  align-items: center;

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    justify-content: center;
  }
`;

const SocialLink = styled(motion.a)`
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.5rem;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);

  &:hover {
    color: white;
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }
`;

const PoweredBy = styled.div`
  position: absolute;
  bottom: ${props => props.theme.spacing.xs};
  right: ${props => props.theme.spacing.md};
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.5);
  display: flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};

  .tech-icon {
    filter: grayscale(1) brightness(0.7);
  }

  @media (max-width: ${props => props.theme.breakpoints.mobile}) {
    position: static;
    justify-content: center;
    margin-top: ${props => props.theme.spacing.sm};
  }
`;

const TechStripes = styled.div`
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, 
    transparent 0%,
    rgba(0, 162, 255, 0.8) 20%, 
    rgba(0, 255, 136, 0.8) 50%, 
    rgba(0, 162, 255, 0.8) 80%,
    transparent 100%
  );
`;

function Footer() {
  const badgeVariants = {
    animate: {
      scale: [1, 1.05, 1],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const socialVariants = {
    hover: {
      scale: 1.1,
      rotate: 5,
      transition: { duration: 0.2 }
    },
    tap: {
      scale: 0.95
    }
  };

  return (
    <FooterContainer>
      <TechStripes />
      <FooterContent>
        <FooterText>
          <span>Made with</span>
          <span className="heart">❤️</span>
          <span>for the Fantastic Four community</span>
        </FooterText>

        <RacingInfo>
          <RacingBadge
            variants={badgeVariants}
            animate="animate"
          >
            🤖 AI Assistant
          </RacingBadge>
          <span>Baxter Building Systems</span>
        </RacingInfo>

        <SocialLinks>
          <SocialLink
            href="#"
            variants={socialVariants}
            whileHover="hover"
            whileTap="tap"
            title="Systems"
          >
            ⚡
          </SocialLink>
          <SocialLink
            href="#"
            variants={socialVariants}
            whileHover="hover"
            whileTap="tap"
            title="Analysis"
          >
            🔬
          </SocialLink>
          <SocialLink
            href="#"
            variants={socialVariants}
            whileHover="hover"
            whileTap="tap"
            title="Database"
          >
            🗃️
          </SocialLink>
        </SocialLinks>
      </FooterContent>

      <PoweredBy>
        <span>Powered by</span>
        <span className="tech-icon">⚛️</span>
        <span>React</span>
        <span>&</span>
        <span className="tech-icon">🐍</span>
        <span>FastAPI</span>
      </PoweredBy>
    </FooterContainer>
  );
}

export default Footer;