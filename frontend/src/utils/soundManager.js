class SoundManager {
  constructor() {
    this.sounds = new Map();
    this.isInitialized = false;
    this.volume = 0.3;
    this.muted = false;
    
    // Sound definitions
    this.soundConfig = {
      engine_start: {
        url: '/sounds/engine_start.mp3',
        volume: 0.4,
        fallback: () => this.playBeep(200, 0.1)
      },
      message_send: {
        url: '/sounds/message_send.mp3',
        volume: 0.2,
        fallback: () => this.playBeep(800, 0.05)
      },
      message_receive: {
        url: '/sounds/message_receive.mp3',
        volume: 0.2,
        fallback: () => this.playBeep(600, 0.05)
      },
      notification: {
        url: '/sounds/notification.mp3',
        volume: 0.3,
        fallback: () => this.playBeep(1000, 0.1)
      },
      error: {
        url: '/sounds/error.mp3',
        volume: 0.4,
        fallback: () => this.playBeep(300, 0.2)
      },
      success: {
        url: '/sounds/success.mp3',
        volume: 0.3,
        fallback: () => this.playBeep(1200, 0.1)
      }
    };
  }

  async initialize() {
    if (this.isInitialized) return;

    try {
      // Check if Web Audio API is supported
      this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
      
      // Load sound files
      await this.loadSounds();
      
      this.isInitialized = true;
      console.log('🔊 Sound Manager initialized successfully');
    } catch (error) {
      console.warn('🔇 Sound Manager initialization failed:', error.message);
      // Continue without sounds - use fallback beeps
      this.isInitialized = true;
    }
  }

  async loadSounds() {
    const loadPromises = Object.entries(this.soundConfig).map(async ([key, config]) => {
      try {
        const audio = new Audio(config.url);
        audio.volume = config.volume * this.volume;
        audio.preload = 'auto';
        
        // Test if the audio can be loaded
        await new Promise((resolve, reject) => {
          audio.addEventListener('canplaythrough', resolve, { once: true });
          audio.addEventListener('error', reject, { once: true });
          audio.load();
        });
        
        this.sounds.set(key, audio);
        console.log(`🎵 Loaded sound: ${key}`);
      } catch (error) {
        console.warn(`⚠️ Could not load sound ${key}:`, error.message);
        // Sound will use fallback beep
      }
    });

    await Promise.allSettled(loadPromises);
  }

  playSound(soundName) {
    if (this.muted || !this.isInitialized) return;

    const audio = this.sounds.get(soundName);
    const config = this.soundConfig[soundName];

    if (audio) {
      try {
        // Reset audio to beginning and play
        audio.currentTime = 0;
        audio.volume = (config.volume || 0.3) * this.volume;
        
        const playPromise = audio.play();
        if (playPromise !== undefined) {
          playPromise.catch(error => {
            console.warn(`🔇 Could not play sound ${soundName}:`, error.message);
            // Fallback to beep
            if (config.fallback) {
              config.fallback();
            }
          });
        }
      } catch (error) {
        console.warn(`🔇 Error playing sound ${soundName}:`, error.message);
        // Fallback to beep
        if (config.fallback) {
          config.fallback();
        }
      }
    } else if (config && config.fallback) {
      // Use fallback beep
      config.fallback();
    }
  }

  // Generate a simple beep sound using Web Audio API
  playBeep(frequency = 800, duration = 0.1) {
    if (this.muted || !this.audioContext) return;

    try {
      const oscillator = this.audioContext.createOscillator();
      const gainNode = this.audioContext.createGain();

      oscillator.connect(gainNode);
      gainNode.connect(this.audioContext.destination);

      oscillator.frequency.value = frequency;
      oscillator.type = 'sine';

      gainNode.gain.setValueAtTime(0, this.audioContext.currentTime);
      gainNode.gain.linearRampToValueAtTime(this.volume * 0.1, this.audioContext.currentTime + 0.01);
      gainNode.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);

      oscillator.start(this.audioContext.currentTime);
      oscillator.stop(this.audioContext.currentTime + duration);
    } catch (error) {
      console.warn('🔇 Could not play beep:', error.message);
    }
  }

  // Play a sequence of beeps (useful for startup sound)
  async playBeepSequence(notes) {
    if (this.muted) return;

    for (const note of notes) {
      this.playBeep(note.frequency, note.duration);
      await this.sleep(note.duration * 1000 + (note.delay || 0));
    }
  }

  // Herbie-specific sound effects
  playEngineStart() {
    // Play startup sequence if no engine sound available
    if (!this.sounds.has('engine_start')) {
      this.playBeepSequence([
        { frequency: 200, duration: 0.3, delay: 100 },
        { frequency: 300, duration: 0.2, delay: 50 },
        { frequency: 400, duration: 0.4, delay: 0 }
      ]);
    } else {
      this.playSound('engine_start');
    }
  }

  playHorn() {
    // Classic car horn pattern
    this.playBeepSequence([
      { frequency: 380, duration: 0.2, delay: 100 },
      { frequency: 320, duration: 0.2, delay: 0 }
    ]);
  }

  playRacingFanfare() {
    // Victory sound
    this.playBeepSequence([
      { frequency: 523, duration: 0.2, delay: 50 },  // C
      { frequency: 659, duration: 0.2, delay: 50 },  // E
      { frequency: 784, duration: 0.2, delay: 50 },  // G
      { frequency: 1047, duration: 0.4, delay: 0 }   // C
    ]);
  }

  // Volume control
  setVolume(volume) {
    this.volume = Math.max(0, Math.min(1, volume));
    
    // Update all loaded sounds
    this.sounds.forEach((audio, key) => {
      const config = this.soundConfig[key];
      audio.volume = (config.volume || 0.3) * this.volume;
    });
    
    console.log(`🔊 Volume set to ${Math.round(this.volume * 100)}%`);
  }

  getVolume() {
    return this.volume;
  }

  // Mute control
  mute() {
    this.muted = true;
    console.log('🔇 Sounds muted');
  }

  unmute() {
    this.muted = false;
    console.log('🔊 Sounds unmuted');
  }

  toggleMute() {
    this.muted = !this.muted;
    console.log(`🔊 Sounds ${this.muted ? 'muted' : 'unmuted'}`);
    return this.muted;
  }

  isMuted() {
    return this.muted;
  }

  // Utility methods
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // Cleanup
  destroy() {
    this.sounds.forEach(audio => {
      audio.pause();
      audio.src = '';
    });
    this.sounds.clear();
    
    if (this.audioContext) {
      this.audioContext.close();
    }
    
    this.isInitialized = false;
    console.log('🔇 Sound Manager destroyed');
  }

  // Get available sounds
  getAvailableSounds() {
    return Array.from(this.sounds.keys());
  }

  // Check if a sound is loaded
  isSoundLoaded(soundName) {
    return this.sounds.has(soundName);
  }
}

// Create singleton instance
export const soundManager = new SoundManager();

// Export class for testing
export default SoundManager;