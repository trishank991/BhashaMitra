'use client';

import { motion } from 'framer-motion';

interface PeppiMascotProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showSpeechBubble?: boolean;
  speechText?: string;
  showAIBadge?: boolean;
  className?: string;
}

const sizes = {
  sm: { container: 'w-24 h-24', svg: 'w-24 h-24' },
  md: { container: 'w-40 h-40', svg: 'w-40 h-40' },
  lg: { container: 'w-64 h-64', svg: 'w-64 h-64' },
  xl: { container: 'w-80 h-80', svg: 'w-80 h-80' },
};

export function PeppiMascot({
  size = 'md',
  showSpeechBubble = false,
  speechText = 'Namaste! I am Peppi!',
  showAIBadge = false,
  className = '',
}: PeppiMascotProps) {
  const { container, svg } = sizes[size];

  return (
    <div className={`relative ${className}`}>
      {/* Glow effect */}
      <motion.div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3/4 h-3/4 bg-orange-300/30 rounded-full blur-3xl"
        animate={{ scale: [1, 1.1, 1], opacity: [0.6, 0.8, 0.6] }}
        transition={{ duration: 3, repeat: Infinity }}
      />

      {/* Peppi character with floating animation */}
      <motion.div
        animate={{ y: [0, -15, 0] }}
        transition={{ duration: 4, repeat: Infinity }}
        className={`relative z-10 ${container}`}
      >
        <svg viewBox="0 0 220 250" xmlns="http://www.w3.org/2000/svg" className={`${svg} drop-shadow-2xl`}>
          {/* Tail */}
          <motion.g
            animate={{ rotate: [-5, 5, -5] }}
            transition={{ duration: 2, repeat: Infinity }}
            style={{ transformOrigin: '155px 160px' }}
          >
            <ellipse fill="#F5E6D3" cx="195" cy="160" rx="25" ry="18" transform="rotate(-20 195 160)"/>
            <ellipse fill="#F5E6D3" cx="205" cy="145" rx="18" ry="14" transform="rotate(-40 205 145)"/>
            <ellipse fill="#F5E6D3" cx="208" cy="125" rx="12" ry="10" transform="rotate(-60 208 125)"/>
          </motion.g>

          {/* Back Paws */}
          <ellipse fill="#F5E6D3" cx="65" cy="215" rx="28" ry="18"/>
          <ellipse fill="#F5E6D3" cx="155" cy="215" rx="28" ry="18"/>
          <ellipse fill="#FFB6C1" cx="55" cy="218" rx="6" ry="5"/>
          <ellipse fill="#FFB6C1" cx="65" cy="222" rx="5" ry="4"/>
          <ellipse fill="#FFB6C1" cx="75" cy="218" rx="6" ry="5"/>
          <ellipse fill="#FFB6C1" cx="65" cy="212" rx="8" ry="6"/>
          <ellipse fill="#FFB6C1" cx="145" cy="218" rx="6" ry="5"/>
          <ellipse fill="#FFB6C1" cx="155" cy="222" rx="5" ry="4"/>
          <ellipse fill="#FFB6C1" cx="165" cy="218" rx="6" ry="5"/>
          <ellipse fill="#FFB6C1" cx="155" cy="212" rx="8" ry="6"/>

          {/* Body */}
          <ellipse fill="#F5E6D3" cx="110" cy="175" rx="65" ry="55"/>

          {/* Head */}
          <ellipse fill="#F5E6D3" cx="110" cy="95" rx="75" ry="70"/>

          {/* Ears */}
          <path fill="#F5E6D3" d="M45 75 L25 15 L75 55 Z"/>
          <path fill="#F5E6D3" d="M175 75 L195 15 L145 55 Z"/>
          <path fill="#E8D4C4" d="M40 55 L28 22 L58 48 Z"/>
          <path fill="#E8D4C4" d="M180 55 L192 22 L162 48 Z"/>
          <path fill="#FFCDB8" d="M48 60 L35 30 L65 52 Z"/>
          <path fill="#FFCDB8" d="M172 60 L185 30 L155 52 Z"/>

          {/* Eyes */}
          <ellipse fill="white" cx="75" cy="95" rx="24" ry="28"/>
          <ellipse fill="white" cx="145" cy="95" rx="24" ry="28"/>
          <motion.ellipse
            fill="#4A90D9"
            cx="75"
            cy="98"
            rx="18"
            ry="22"
            animate={{ ry: [22, 20, 22] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.ellipse
            fill="#4A90D9"
            cx="145"
            cy="98"
            rx="18"
            ry="22"
            animate={{ ry: [22, 20, 22] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <ellipse fill="#1a1a1a" cx="75" cy="100" rx="8" ry="10"/>
          <ellipse fill="#1a1a1a" cx="145" cy="100" rx="8" ry="10"/>
          <circle fill="white" cx="82" cy="88" r="7"/>
          <circle fill="white" cx="152" cy="88" r="7"/>
          <circle fill="white" cx="70" cy="102" r="4"/>
          <circle fill="white" cx="140" cy="102" r="4"/>

          {/* Nose */}
          <path fill="#FF7F50" d="M110 115 L103 128 L117 128 Z"/>

          {/* Whiskers */}
          <motion.g
            animate={{ x: [-2, 2, -2] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="20" y1="105" x2="55" y2="112"/>
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="18" y1="118" x2="55" y2="120"/>
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="20" y1="131" x2="55" y2="128"/>
          </motion.g>
          <motion.g
            animate={{ x: [2, -2, 2] }}
            transition={{ duration: 2, repeat: Infinity }}
          >
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="200" y1="105" x2="165" y2="112"/>
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="202" y1="118" x2="165" y2="120"/>
            <line stroke="#999" strokeWidth="1.5" strokeLinecap="round" x1="200" y1="131" x2="165" y2="128"/>
          </motion.g>

          {/* Collar */}
          <ellipse fill="#FF6B35" cx="110" cy="148" rx="45" ry="8"/>
          <rect fill="#FF6B35" x="65" y="144" width="90" height="8" rx="4"/>

          {/* Bell */}
          <motion.g
            animate={{ rotate: [-5, 5, -5] }}
            transition={{ duration: 0.5, repeat: Infinity }}
            style={{ transformOrigin: '110px 158px' }}
          >
            <circle fill="#FFD700" cx="110" cy="158" r="10"/>
            <circle fill="#FFF8DC" cx="107" cy="155" r="3"/>
            <line stroke="#B8860B" strokeWidth="2" x1="110" y1="165" x2="110" y2="168"/>
            <rect fill="#B8860B" x="105" y="148" width="10" height="6" rx="2"/>
          </motion.g>
        </svg>
      </motion.div>

      {/* Speech bubble */}
      {showSpeechBubble && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="absolute top-0 right-0 sm:-right-4"
        >
          <motion.div
            animate={{ y: [0, -8, 0], rotate: [-2, 2, -2] }}
            transition={{ duration: 3, repeat: Infinity }}
            className="bg-white px-4 py-3 rounded-2xl shadow-lg font-bold text-teal-800 text-sm"
          >
            {speechText}
            <div className="absolute bottom-0 left-8 w-0 h-0 border-l-[12px] border-l-transparent border-r-[12px] border-r-transparent border-t-[12px] border-t-white -mb-3" />
          </motion.div>
        </motion.div>
      )}

      {/* AI Badge */}
      {showAIBadge && (
        <motion.div
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.8 }}
          className="absolute bottom-4 left-4"
        >
          <motion.div
            animate={{ scale: [1, 1.05, 1] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="bg-gradient-to-r from-pink-500 to-orange-500 text-white px-3 py-1.5 rounded-full text-xs font-bold shadow-lg"
          >
            AI Powered
          </motion.div>
        </motion.div>
      )}
    </div>
  );
}

export default PeppiMascot;
