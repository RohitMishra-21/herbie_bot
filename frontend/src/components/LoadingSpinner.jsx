import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const SpinnerContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: ${props => props.fullHeight ? '100vh' : '200px'};
  padding: ${props => props.theme.spacing.xl};
  text-align: center;
`;

const CarContainer = styled(motion.div)`
  position: relative;
  margin-bottom: ${props => props.theme.spacing.xl};
`;

const Car = styled(motion.div)`
  font-size: 4rem;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
  position: relative;
  z-index: 2;
`;

const Road = styled.div`
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 50px;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.8), transparent);
    animation: roadShine 2s infinite linear;
  }

  @keyframes roadShine {
    0% { left: -100%; }
    100% { left: 100%; }
  }
`;

const Smoke = styled(motion.div)`
  position: absolute;
  bottom: 0;
  left: -20px;
  font-size: 1.5rem;
  opacity: 0.6;
`;

const LoadingText = styled(motion.div)`
  color: white;
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: ${props => props.theme.spacing.md};
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const SubText = styled(motion.div)`
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  max-width: 300px;
  line-height: 1.5;
`;

const ProgressBar = styled.div`
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  margin-top: ${props => props.theme.spacing.lg};
  overflow: hidden;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: linear-gradient(90deg, 
    ${props => props.theme.colors.primary}, 
    ${props => props.theme.colors.secondary},
    ${props => props.theme.colors.accent}
  );
  border-radius: 2px;
`;

const RacingFlags = styled.div`
  position: absolute;
  top: -30px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: ${props => props.theme.spacing.xs};
`;

const Flag = styled(motion.div)`
  font-size: 1.5rem;
  opacity: 0.7;
`;

function LoadingSpinner({ 
  message = "Starting up Herbie...", 
  subMessage = "Please wait while we fire up the engine!",
  fullHeight = false,
  showProgress = false
}) {
  const carVariants = {
    animate: {
      x: [0, 20, 0],
      rotate: [0, 2, -2, 0],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const smokeVariants = {
    animate: {
      x: [0, -10, -20, -30],
      opacity: [0.6, 0.4, 0.2, 0],
      scale: [1, 1.2, 1.4, 1.6],
      transition: {
        duration: 1,
        repeat: Infinity,
        ease: "easeOut"
      }
    }
  };

  const textVariants = {
    animate: {
      opacity: [1, 0.7, 1],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  const flagVariants = {
    animate: (i) => ({
      rotate: [0, 10, -10, 0],
      transition: {
        duration: 1.5,
        repeat: Infinity,
        delay: i * 0.2,
        ease: "easeInOut"
      }
    })
  };

  const progressVariants = {
    animate: {
      width: ["0%", "100%"],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut"
      }
    }
  };

  return (
    <SpinnerContainer fullHeight={fullHeight}>
      <CarContainer>
        <RacingFlags>
          <Flag
            variants={flagVariants}
            animate="animate"
            custom={0}
          >
            🏁
          </Flag>
          <Flag
            variants={flagVariants}
            animate="animate"
            custom={1}
          >
            🏁
          </Flag>
        </RacingFlags>
        
        <Car
          variants={carVariants}
          animate="animate"
        >
          🚗
        </Car>
        
        <Smoke
          variants={smokeVariants}
          animate="animate"
        >
          💨
        </Smoke>
        
        <Road />
      </CarContainer>

      <LoadingText
        variants={textVariants}
        animate="animate"
      >
        {message}
      </LoadingText>

      <SubText
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5, duration: 0.8 }}
      >
        {subMessage}
      </SubText>

      {showProgress && (
        <ProgressBar>
          <ProgressFill
            variants={progressVariants}
            animate="animate"
          />
        </ProgressBar>
      )}
    </SpinnerContainer>
  );
}

export default LoadingSpinner;