/**
 * Sound Effects Service for BhashaMitra
 *
 * Provides UI sound feedback for learning interactions.
 * Sounds are played for correct/wrong answers, achievements,
 * level ups, and other gamification events.
 *
 * Usage:
 *   import { soundService } from '@/lib/soundService';
 *   soundService.play('correct');
 *   // or use convenience methods:
 *   soundService.onCorrect();
 */

export type SoundName =
  | 'correct'
  | 'wrong'
  | 'levelUp'
  | 'badge'
  | 'click'
  | 'pageTurn'
  | 'celebration'
  | 'meow'
  | 'streak'
  | 'storyComplete'
  | 'pop'
  | 'whoosh'
  | 'recordStart'
  | 'recordStop';

// Sound file paths (relative to public directory)
const SOUND_PATHS: Record<SoundName, string> = {
  correct: '/audio/sounds/correct.wav',
  wrong: '/audio/sounds/wrong.wav',
  levelUp: '/audio/sounds/level-up.wav',
  badge: '/audio/sounds/badge.wav',
  click: '/audio/sounds/click.wav',
  pageTurn: '/audio/sounds/page-turn.wav',
  celebration: '/audio/sounds/celebration.wav',
  meow: '/audio/sounds/meow.wav',
  streak: '/audio/sounds/streak.wav',
  storyComplete: '/audio/sounds/story-complete.wav',
  pop: '/audio/sounds/pop.wav',
  whoosh: '/audio/sounds/whoosh.wav',
  recordStart: '/audio/sounds/pop.wav', // Use pop for record start
  recordStop: '/audio/sounds/click.wav', // Use click for record stop
};

// Default volume levels for different sounds
const DEFAULT_VOLUMES: Partial<Record<SoundName, number>> = {
  click: 0.3,
  pageTurn: 0.4,
  wrong: 0.5,
  meow: 0.6,
  pop: 0.4,
  whoosh: 0.4,
};

class SoundService {
  private audioCache: Map<SoundName, HTMLAudioElement> = new Map();
  private enabled: boolean = true;
  private globalVolume: number = 0.7;
  private initialized: boolean = false;
  private _userHasInteracted: boolean = false;
  private audioContext: AudioContext | null = null;

  constructor() {
    // Load settings from localStorage on client side
    if (typeof window !== 'undefined') {
      const savedEnabled = localStorage.getItem('bhashamitra_sounds_enabled');
      this.enabled = savedEnabled !== 'false';

      const savedVolume = localStorage.getItem('bhashamitra_sounds_volume');
      if (savedVolume) {
        this.globalVolume = parseFloat(savedVolume);
      }

      // Track user interaction to enable autoplay
      const enableAudio = () => {
        this._userHasInteracted = true;
        // Play a silent audio to unlock audio context
        const silentAudio = new Audio();
        silentAudio.play().catch(() => {});
      };

      // Listen for first user interaction
      ['click', 'touchstart', 'keydown'].forEach(event => {
        document.addEventListener(event, enableAudio, { once: true, passive: true });
      });
    }
  }

  /**
   * Initialize and preload all sounds for instant playback.
   * Call this once when the app loads.
   */
  preload(): void {
    if (typeof window === 'undefined' || this.initialized) return;

    Object.entries(SOUND_PATHS).forEach(([name, path]) => {
      try {
        const audio = new Audio(path);
        audio.preload = 'auto';
        // Attach error handler to gracefully handle missing files
        audio.onerror = () => {
          console.warn(`[SoundService] Sound file not found: ${path}`);
        };
        this.audioCache.set(name as SoundName, audio);
      } catch (error) {
        console.warn(`[SoundService] Failed to preload ${name}:`, error);
      }
    });

    this.initialized = true;
  }

  /**
   * Play a sound effect.
   * @param sound - The sound to play
   * @param volume - Optional volume override (0-1)
   */
  play(sound: SoundName, volume?: number): void {
    if (!this.enabled || typeof window === 'undefined') return;

    try {
      let audio = this.audioCache.get(sound);

      // Lazy load if not preloaded
      if (!audio) {
        const path = SOUND_PATHS[sound];
        if (!path) {
          console.warn(`[SoundService] Unknown sound: ${sound}`);
          return;
        }
        audio = new Audio(path);
        this.audioCache.set(sound, audio);
      }

      // Clone the audio element to allow overlapping playback
      const clone = audio.cloneNode() as HTMLAudioElement;

      // Calculate final volume
      const baseVolume = DEFAULT_VOLUMES[sound] ?? 0.7;
      clone.volume = Math.min(1, Math.max(0, (volume ?? baseVolume) * this.globalVolume));

      // Play and handle errors gracefully
      clone.play().catch((error) => {
        // Handle specific error types
        if (error instanceof DOMException) {
          // NotSupportedError - audio format/browser doesn't support it
          if (error.name === 'NotSupportedError') {
            console.warn(`[SoundService] Audio format not supported for ${sound}, skipping`);
            return;
          }
          // NotAllowedError - autoplay blocked
          if (error.name === 'NotAllowedError') {
            // Silently ignore autoplay errors
            return;
          }
        }
        // Log other errors
        console.warn(`[SoundService] Failed to play ${sound}:`, error);
      });
    } catch (error) {
      console.warn(`[SoundService] Error playing ${sound}:`, error);
    }
  }

  /**
   * Enable or disable all sounds.
   */
  setEnabled(enabled: boolean): void {
    this.enabled = enabled;
    if (typeof window !== 'undefined') {
      localStorage.setItem('bhashamitra_sounds_enabled', String(enabled));
    }
  }

  /**
   * Toggle sounds on/off.
   */
  toggle(): boolean {
    this.setEnabled(!this.enabled);
    return this.enabled;
  }

  /**
   * Check if sounds are enabled.
   */
  isEnabled(): boolean {
    return this.enabled;
  }

  /**
   * Set the global volume for all sounds.
   * @param volume - Volume level (0-1)
   */
  setVolume(volume: number): void {
    this.globalVolume = Math.min(1, Math.max(0, volume));
    if (typeof window !== 'undefined') {
      localStorage.setItem('bhashamitra_sounds_volume', String(this.globalVolume));
    }
  }

  /**
   * Get the current global volume.
   */
  getVolume(): number {
    return this.globalVolume;
  }

  // =========================================================================
  // Convenience Methods - Use these in components
  // =========================================================================

  /** Play when user answers correctly */
  onCorrect(): void {
    this.play('correct');
  }

  /** Play when user answers incorrectly */
  onWrong(): void {
    this.play('wrong');
  }

  /** Play when user levels up */
  onLevelUp(): void {
    this.play('levelUp');
  }

  /** Play when user earns a badge */
  onBadge(): void {
    this.play('badge');
  }

  /** Play on button/UI clicks */
  onClick(): void {
    this.play('click');
  }

  /** Play when turning story pages */
  onPageTurn(): void {
    this.play('pageTurn');
  }

  /** Play for celebrations (level complete, story done, etc.) */
  onCelebration(): void {
    this.play('celebration');
  }

  /** Play Peppi's meow sound */
  onPeppiMeow(): void {
    this.play('meow');
  }

  /** Play when user hits a streak milestone */
  onStreak(): void {
    this.play('streak');
  }

  /** Play when a story is completed */
  onStoryComplete(): void {
    this.play('storyComplete');
  }

  /** Play a pop sound (bubbles, selections, etc.) */
  onPop(): void {
    this.play('pop');
  }

  /** Play a whoosh sound (transitions, swipes) */
  onWhoosh(): void {
    this.play('whoosh');
  }

  // =========================================================================
  // Mimic Practice Sound Methods
  // =========================================================================

  /**
   * Get or create the Web Audio API context for synthesized sounds
   */
  private getAudioContext(): AudioContext | null {
    if (typeof window === 'undefined') return null;

    if (!this.audioContext) {
      try {
        this.audioContext = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
      } catch (error) {
        console.warn('[SoundService] Failed to create AudioContext:', error);
        return null;
      }
    }

    // Resume context if suspended (required by browsers after user interaction)
    if (this.audioContext.state === 'suspended') {
      this.audioContext.resume().catch(() => {});
    }

    return this.audioContext;
  }

  /**
   * Play a synthesized tone using Web Audio API
   */
  private playTone(
    frequency: number,
    duration: number,
    type: OscillatorType = 'sine',
    volume: number = 0.3
  ): void {
    if (!this.enabled) return;

    const ctx = this.getAudioContext();
    if (!ctx) return;

    try {
      const oscillator = ctx.createOscillator();
      const gainNode = ctx.createGain();

      oscillator.type = type;
      oscillator.frequency.setValueAtTime(frequency, ctx.currentTime);

      const adjustedVolume = volume * this.globalVolume;
      gainNode.gain.setValueAtTime(adjustedVolume, ctx.currentTime);
      gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + duration);

      oscillator.connect(gainNode);
      gainNode.connect(ctx.destination);

      oscillator.start(ctx.currentTime);
      oscillator.stop(ctx.currentTime + duration);
    } catch (error) {
      console.warn('[SoundService] Tone playback failed:', error);
    }
  }

  /**
   * Play countdown beep (3, 2, 1) - higher pitch as countdown progresses
   */
  playCountdownBeep(count: number): void {
    const frequencies: Record<number, number> = {
      3: 523,  // C5
      2: 659,  // E5
      1: 784,  // G5 - highest pitch for "1"
    };
    this.playTone(frequencies[count] || 523, 0.12, 'sine', 0.5);
  }

  /**
   * Play sound when recording starts
   */
  onRecordingStart(): void {
    if (!this.enabled) return;

    const ctx = this.getAudioContext();
    if (!ctx) {
      // Fallback to file-based sound
      this.play('recordStart', 0.5);
      return;
    }

    try {
      // Quick ascending notes (C5, E5, G5) - "go!" sound
      const notes = [523, 659, 784];
      const adjustedVolume = 0.35 * this.globalVolume;

      notes.forEach((freq, i) => {
        const oscillator = ctx.createOscillator();
        const gainNode = ctx.createGain();

        oscillator.type = 'sine';
        oscillator.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.07);

        gainNode.gain.setValueAtTime(adjustedVolume, ctx.currentTime + i * 0.07);
        gainNode.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + i * 0.07 + 0.12);

        oscillator.connect(gainNode);
        gainNode.connect(ctx.destination);

        oscillator.start(ctx.currentTime + i * 0.07);
        oscillator.stop(ctx.currentTime + i * 0.07 + 0.12);
      });
    } catch {
      this.play('recordStart', 0.5);
    }
  }

  /**
   * Play sound when recording stops
   */
  onRecordingStop(): void {
    this.playTone(784, 0.15, 'sine', 0.4); // G5 - single note
  }

  /**
   * Play sound for each star earned (during result display)
   */
  playStarEarned(starIndex: number): void {
    // Each star gets a higher note - creates a pleasant ascending effect
    const frequencies = [523, 659, 784]; // C5, E5, G5
    setTimeout(() => {
      this.playTone(frequencies[starIndex] || 523, 0.2, 'triangle', 0.4);
    }, starIndex * 200); // Stagger the sounds
  }

  /**
   * Play result sound based on stars earned
   */
  playMimicResult(stars: number): void {
    if (!this.enabled) return;

    if (stars === 3) {
      // Perfect - play celebration
      this.play('celebration');
    } else if (stars === 2) {
      // Good - play correct sound
      this.play('correct');
    } else if (stars === 1) {
      // Okay - play streak (encouraging)
      this.play('streak', 0.5);
    } else {
      // Try again - play gentle wrong sound
      this.play('wrong', 0.4);
    }
  }

  /**
   * Play all stars sound sequence
   */
  playStarsSequence(totalStars: number): void {
    for (let i = 0; i < totalStars; i++) {
      this.playStarEarned(i);
    }
  }
}

// Export singleton instance
export const soundService = new SoundService();

// Export class for testing
export { SoundService };
