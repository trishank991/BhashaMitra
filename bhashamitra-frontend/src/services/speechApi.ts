/**
 * Speech API service for STT (Speech-to-Text) with pronunciation evaluation.
 *
 * This service provides:
 * - Audio transcription via Google Cloud STT
 * - Pronunciation evaluation with enhanced feedback
 * - Child-friendly messages in Hindi and English
 * - Word-by-word comparison with phonetic hints
 */

import api from '@/lib/api';

// ============================================
// TYPE DEFINITIONS
// ============================================

export interface WordComparison {
  expected: string;
  expected_roman: string;
  heard: string;
  heard_roman: string;
  is_correct: boolean;
  similarity: number;
  hint?: string | null;
}

export interface PronunciationFeedback {
  level: 'excellent' | 'good' | 'okay' | 'try_again';
  emoji: string;
  message_hindi: string;
  message_english: string;
  encouragement: string;
}

export interface PronunciationEvaluation {
  score: number;
  similarity: number;
  confidence: number;
  stars: number;
  is_correct: boolean;
  expected: {
    native: string;
    roman: string;
  };
  heard: {
    native: string;
    roman: string;
  };
  feedback: PronunciationFeedback;
  word_comparison: WordComparison[];
  hints: string[];
  attempt_number: number;
}

export interface STTResponse {
  success: boolean;
  error?: string;
  data: {
    transcription: string;
    confidence: number;
    provider?: string;
    duration_ms?: number;
    evaluation?: PronunciationEvaluation;
  };
}

export interface STTRequest {
  audio_url: string;
  language: string;
  expected_text?: string;
  attempt_number?: number;
}

// ============================================
// HELPER FUNCTIONS
// ============================================

/**
 * Convert a Blob to base64 string.
 * Useful for sending audio data to APIs that expect base64.
 */
export async function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => {
      const base64 = (reader.result as string).split(',')[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

// ============================================
// SPEECH API CLASS
// ============================================

class SpeechApiService {
  /**
   * Upload audio file and get URL.
   *
   * @param childId - Child's UUID
   * @param audioBlob - Audio blob from recording
   * @param filename - Optional filename
   * @returns URL of the uploaded audio
   */
  async uploadAudio(
    childId: string,
    audioBlob: Blob,
    filename: string = 'recording.webm'
  ): Promise<{ success: boolean; audioUrl?: string; error?: string }> {
    try {
      const result = await api.uploadMimicAudio(childId, audioBlob, filename);

      if (result.success && result.data?.audio_url) {
        return {
          success: true,
          audioUrl: result.data.audio_url,
        };
      }

      return {
        success: false,
        error: result.error || 'Failed to upload audio',
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }

  /**
   * Transcribe audio and optionally evaluate pronunciation.
   *
   * @param request - STT request parameters
   * @returns Transcription and optional pronunciation evaluation
   */
  async transcribe(request: STTRequest): Promise<STTResponse> {
    try {
      const response = await api.transcribeSpeech(
        request.audio_url,
        request.language,
        request.expected_text,
        request.attempt_number
      );

      if (response.success && response.data) {
        return {
          success: true,
          data: {
            transcription: response.data.transcription,
            confidence: response.data.confidence,
            provider: response.data.provider,
            duration_ms: response.data.duration_ms,
            evaluation: response.data.evaluation as PronunciationEvaluation | undefined,
          },
        };
      }

      return {
        success: false,
        error: response.error || 'Transcription failed',
        data: {
          transcription: '',
          confidence: 0,
        },
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Transcription failed',
        data: {
          transcription: '',
          confidence: 0,
        },
      };
    }
  }

  /**
   * Full pronunciation practice flow:
   * 1. Upload audio
   * 2. Transcribe and evaluate
   *
   * @param childId - Child's UUID
   * @param audioBlob - Audio blob from recording
   * @param language - Language code (HINDI, TAMIL, etc.)
   * @param expectedText - The text the child should have said
   * @param attemptNumber - Which attempt this is (for varied feedback)
   * @returns Pronunciation evaluation results
   */
  async evaluatePronunciation(
    childId: string,
    audioBlob: Blob,
    language: string,
    expectedText: string,
    attemptNumber: number = 1
  ): Promise<{
    success: boolean;
    evaluation?: PronunciationEvaluation;
    transcription?: string;
    error?: string;
  }> {
    // Step 1: Upload audio
    const uploadResult = await this.uploadAudio(childId, audioBlob);

    if (!uploadResult.success || !uploadResult.audioUrl) {
      return {
        success: false,
        error: uploadResult.error || 'Failed to upload audio',
      };
    }

    // Step 2: Transcribe and evaluate
    const sttResult = await this.transcribe({
      audio_url: uploadResult.audioUrl,
      language,
      expected_text: expectedText,
      attempt_number: attemptNumber,
    });

    if (!sttResult.success) {
      return {
        success: false,
        error: sttResult.error || 'Failed to process audio',
      };
    }

    return {
      success: true,
      transcription: sttResult.data.transcription,
      evaluation: sttResult.data.evaluation,
    };
  }
}

// Export singleton instance
export const speechApi = new SpeechApiService();
export default speechApi;
