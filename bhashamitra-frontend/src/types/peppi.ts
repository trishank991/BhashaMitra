// Peppi AI Types for Interactive Learning

export type PeppiExpression = 'happy' | 'excited' | 'thinking' | 'encouraging' | 'celebrating' | 'waving' | 'proud' | 'thoughtful';

export type PeppiMood = 'happy' | 'excited' | 'thinking' | 'encouraging' | 'celebrating' | 'sleepy' | 'neutral';

export interface PeppiContext {
  id: string;
  child: string;
  child_name: string;
  child_age: number;
  current_topic: string;
  words_taught_today: string[];
  mistakes_made: string[];
  mood: PeppiMood;
  last_interaction: string;
  total_sessions: number;
  streak_days: number;
  created_at: string;
  updated_at: string;
}

export interface PeppiGreeting {
  greeting_hindi: string;
  greeting_romanized: string;
  greeting_english: string;
  message_hindi: string;
  message_romanized: string;
  message_english: string;
  expression: PeppiExpression;
  peppi_mood: PeppiMood;
  session_count: number;
  streak: number;
  audio_url?: string;
}

export interface PeppiTeaching {
  word_hindi: string;
  word_romanized: string;
  word_english: string;
  teaching_script_hindi: string;
  teaching_script_romanized: string;
  teaching_script_english: string;
  part_of_speech: string;
  audio_url: string;
  example_sentence: string;
}

export interface PeppiFeedback {
  feedback_hindi: string;
  feedback_romanized: string;
  feedback_english: string;
  is_correct: boolean;
  expression: PeppiExpression;
  message_hindi: string;
  message_romanized: string;
  message_english: string;
  audio_url?: string;
}

export interface PeppiResponse {
  text_hindi: string;
  text_romanized: string;
  text_english?: string;
  expression: PeppiExpression;
  audio_url?: string;
  actions?: string[];
}

// ===================================
// Peppi Chat Types (AI Chatbot)
// ===================================

export type PeppiChatMode = 'FESTIVAL_STORY' | 'CURRICULUM_HELP' | 'GENERAL';

export type MessageRole = 'user' | 'assistant' | 'system';

export type InputType = 'text' | 'voice';

export interface PeppiChatMessage {
  id: string;
  role: MessageRole;
  content_primary: string;
  content_romanized?: string;
  content_english?: string;
  audio_input_url?: string;
  audio_output_url?: string;
  input_type: InputType;
  created_at: string;
}

export interface PeppiConversation {
  id: string;
  child_name: string;
  mode: PeppiChatMode;
  language: string;
  festival?: string;
  story?: string;
  lesson?: string;
  is_active: boolean;
  messages_count: number;
  created_at: string;
  last_message_at: string;
  messages?: PeppiChatMessage[];
}

export interface PeppiConversationListItem {
  id: string;
  child_name: string;
  mode: PeppiChatMode;
  language: string;
  is_active: boolean;
  messages_count: number;
  created_at: string;
  last_message_at: string;
  last_message?: {
    role: MessageRole;
    content: string;
    created_at: string;
  };
}

export interface StartConversationRequest {
  mode: PeppiChatMode;
  language?: string;
  festival_id?: string;
  story_id?: string;
  lesson_id?: string;
}

export interface StartConversationResponse {
  conversation: PeppiConversation;
  greeting: PeppiChatMessage;
}

export interface SendMessageRequest {
  content: string;
  input_type?: InputType;
  audio_url?: string;
}

export interface SendMessageResponse {
  user_message: PeppiChatMessage;
  assistant_message: PeppiChatMessage;
  was_moderated: boolean;
  needs_escalation: boolean;
}

export interface ConversationHistoryResponse {
  conversation: PeppiConversationListItem;
  messages: PeppiChatMessage[];
  has_more: boolean;
  total_messages: number;
}

export interface PeppiChatStatusResponse {
  available: boolean;
  gemini_status: 'online' | 'offline';
  tier_access: boolean;
  message: string;
}

// ===================================
// Escalation Types
// ===================================

export type EscalationStatus = 'PENDING' | 'IN_PROGRESS' | 'RESOLVED' | 'CLOSED';

export interface SubmitEscalationRequest {
  message_id?: string;
  description: string;
}

export interface PeppiEscalationReport {
  id: string;
  child_name: string;
  conversation: string;
  message?: string;
  user_description: string;
  conversation_mode: PeppiChatMode;
  status: EscalationStatus;
  admin_response: string;
  created_at: string;
  resolved_at?: string;
}

export interface SubmitEscalationResponse {
  escalation: PeppiEscalationReport;
  message: string;
}
