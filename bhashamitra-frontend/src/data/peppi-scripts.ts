import { AgeVariant } from '@/hooks/useAgeConfig';

export type PeppiMood = 'happy' | 'excited' | 'thinking' | 'encouraging' | 'celebrating' | 'sleepy';

export interface PeppiScript {
  message: string;
  mood: PeppiMood;
  audioText?: string; // Text to speak (may differ from display message)
}

export interface PeppiScriptSet {
  welcome: PeppiScript[];
  correct: PeppiScript[];
  incorrect: PeppiScript[];
  encouragement: PeppiScript[];
  lessonComplete: PeppiScript[];
  streak: PeppiScript[];
  hint: PeppiScript[];
  idle: PeppiScript[];
}

// Age-specific Peppi scripts
const SCRIPTS: Record<AgeVariant, PeppiScriptSet> = {
  junior: {
    welcome: [
      { message: "Hi friend! Let's play and learn!", mood: 'excited', audioText: 'Hi friend! Lets play and learn together!' },
      { message: "Yay! Learning time! 🎉", mood: 'celebrating', audioText: 'Yay! Its learning time!' },
      { message: "I'm so happy to see you!", mood: 'happy', audioText: 'I am so happy to see you!' },
    ],
    correct: [
      { message: "WOW! You did it! ⭐", mood: 'celebrating', audioText: 'Wow! You did it! Amazing!' },
      { message: "Super duper! 🌟", mood: 'excited', audioText: 'Super duper! Great job!' },
      { message: "You're amazing!", mood: 'celebrating', audioText: 'You are amazing!' },
      { message: "Yippee! Correct! 🎊", mood: 'excited', audioText: 'Yippee! That is correct!' },
    ],
    incorrect: [
      { message: "Oopsie! Try again!", mood: 'encouraging', audioText: 'Oopsie! Lets try again!' },
      { message: "Almost! One more try!", mood: 'encouraging', audioText: 'Almost there! One more try!' },
      { message: "You can do it!", mood: 'happy', audioText: 'I know you can do it!' },
    ],
    encouragement: [
      { message: "You're doing great!", mood: 'happy', audioText: 'You are doing great!' },
      { message: "Keep going! 💪", mood: 'encouraging', audioText: 'Keep going! You got this!' },
      { message: "I believe in you!", mood: 'encouraging', audioText: 'I believe in you!' },
    ],
    lessonComplete: [
      { message: "Hooray! All done! 🏆", mood: 'celebrating', audioText: 'Hooray! You finished the lesson! Great job!' },
      { message: "You're a superstar! ⭐", mood: 'celebrating', audioText: 'You are a superstar!' },
    ],
    streak: [
      { message: "Wow! 3 in a row! 🔥", mood: 'excited', audioText: 'Wow! Three in a row! Amazing!' },
      { message: "You're on fire! 🌟", mood: 'celebrating', audioText: 'You are on fire! Keep it up!' },
    ],
    hint: [
      { message: "Psst! Listen again!", mood: 'thinking', audioText: 'Psst! Try listening again!' },
      { message: "Let me help you!", mood: 'happy', audioText: 'Let me help you!' },
    ],
    idle: [
      { message: "Tap me to play! 🐱", mood: 'happy', audioText: 'Tap me to play!' },
      { message: "*yawns* Let's learn!", mood: 'sleepy', audioText: 'Yawns. Lets learn something new!' },
    ],
  },
  standard: {
    welcome: [
      { message: "Hey! Ready to learn Hindi?", mood: 'happy', audioText: 'Hey! Ready to learn Hindi today?' },
      { message: "Let's discover something new!", mood: 'excited', audioText: 'Lets discover something new today!' },
      { message: "Welcome back, learner!", mood: 'happy', audioText: 'Welcome back, learner!' },
    ],
    correct: [
      { message: "Excellent work! 🌟", mood: 'celebrating', audioText: 'Excellent work!' },
      { message: "That's right! Well done!", mood: 'happy', audioText: 'Thats right! Well done!' },
      { message: "Perfect! Keep it up!", mood: 'excited', audioText: 'Perfect! Keep it up!' },
      { message: "शाबाश! (Shabash!)", mood: 'celebrating', audioText: 'Shabash! Great job!' },
    ],
    incorrect: [
      { message: "Not quite. Try again!", mood: 'encouraging', audioText: 'Not quite right. Try again!' },
      { message: "Close! Listen carefully.", mood: 'thinking', audioText: 'Close! Listen carefully and try again.' },
      { message: "Keep trying!", mood: 'encouraging', audioText: 'Keep trying! You can do it!' },
    ],
    encouragement: [
      { message: "You're making progress!", mood: 'happy', audioText: 'You are making great progress!' },
      { message: "Every mistake helps you learn!", mood: 'encouraging', audioText: 'Every mistake helps you learn!' },
      { message: "Stay focused!", mood: 'thinking', audioText: 'Stay focused! You got this!' },
    ],
    lessonComplete: [
      { message: "Lesson complete! Great job! 🏆", mood: 'celebrating', audioText: 'Lesson complete! Great job!' },
      { message: "You mastered this! 🎯", mood: 'celebrating', audioText: 'You mastered this lesson!' },
    ],
    streak: [
      { message: "5 correct in a row! 🔥", mood: 'excited', audioText: 'Five correct in a row! Amazing!' },
      { message: "You're on a roll!", mood: 'celebrating', audioText: 'You are on a roll!' },
    ],
    hint: [
      { message: "Need a hint? Listen again!", mood: 'thinking', audioText: 'Need a hint? Try listening again!' },
      { message: "Focus on the sound...", mood: 'thinking', audioText: 'Focus on the sound.' },
    ],
    idle: [
      { message: "Ready when you are!", mood: 'happy', audioText: 'Ready when you are!' },
      { message: "Take your time.", mood: 'thinking', audioText: 'Take your time.' },
    ],
  },
  teen: {
    welcome: [
      { message: "Let's level up your Hindi!", mood: 'happy', audioText: 'Lets level up your Hindi!' },
      { message: "Ready for today's challenge?", mood: 'excited', audioText: 'Ready for todays challenge?' },
      { message: "Time to practice!", mood: 'happy', audioText: 'Time to practice!' },
    ],
    correct: [
      { message: "Correct! Nice work.", mood: 'happy', audioText: 'Correct! Nice work.' },
      { message: "You got it! 👍", mood: 'happy', audioText: 'You got it!' },
      { message: "Well done.", mood: 'happy', audioText: 'Well done.' },
      { message: "बहुत अच्छा! (Very good!)", mood: 'celebrating', audioText: 'Bahut accha! Very good!' },
    ],
    incorrect: [
      { message: "Not quite. Review and retry.", mood: 'thinking', audioText: 'Not quite right. Review and try again.' },
      { message: "Almost there!", mood: 'encouraging', audioText: 'Almost there!' },
      { message: "Try a different approach.", mood: 'thinking', audioText: 'Try a different approach.' },
    ],
    encouragement: [
      { message: "You're improving!", mood: 'happy', audioText: 'You are improving!' },
      { message: "Consistency is key!", mood: 'encouraging', audioText: 'Consistency is key!' },
      { message: "Keep pushing forward!", mood: 'encouraging', audioText: 'Keep pushing forward!' },
    ],
    lessonComplete: [
      { message: "Lesson done! 🎯", mood: 'celebrating', audioText: 'Lesson complete!' },
      { message: "Another one completed!", mood: 'happy', audioText: 'Another lesson completed!' },
    ],
    streak: [
      { message: "10 streak! Impressive! 🔥", mood: 'excited', audioText: 'Ten in a row! Impressive!' },
      { message: "You're crushing it!", mood: 'celebrating', audioText: 'You are crushing it!' },
    ],
    hint: [
      { message: "Think about the context.", mood: 'thinking', audioText: 'Think about the context.' },
      { message: "Review the pattern.", mood: 'thinking', audioText: 'Review the pattern.' },
    ],
    idle: [
      { message: "Ready to continue?", mood: 'happy', audioText: 'Ready to continue?' },
      { message: "Let's keep going.", mood: 'happy', audioText: 'Lets keep going.' },
    ],
  },
};

export function getPeppiScripts(ageVariant: AgeVariant): PeppiScriptSet {
  return SCRIPTS[ageVariant];
}

export function getRandomScript(scripts: PeppiScript[]): PeppiScript {
  return scripts[Math.floor(Math.random() * scripts.length)];
}

export default SCRIPTS;
