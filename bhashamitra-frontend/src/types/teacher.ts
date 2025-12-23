/**
 * Live classes and teacher types
 */

export type TeacherStatus = 'PENDING' | 'VERIFIED' | 'SUSPENDED' | 'INACTIVE';

export type SessionType = 'ONE_ON_ONE' | 'GROUP' | 'CULTURAL_EVENT';

export type SessionStatus = 'SCHEDULED' | 'IN_PROGRESS' | 'COMPLETED' | 'CANCELLED' | 'NO_SHOW';

export type ParticipantStatus = 'REGISTERED' | 'ATTENDED' | 'NO_SHOW' | 'CANCELLED';

export interface Teacher {
  id: string;
  userId: string;
  displayName: string;
  bio: string;
  profileImage: string;
  languages: string[];
  specializations: string[];
  status: TeacherStatus;
  hourlyRate: number;
  rating: number;
  totalSessions: number;
  totalStudents: number;
  verifiedAt: string | null;
}

export interface TeacherCertification {
  id: string;
  teacherId: string;
  title: string;
  issuingOrganization: string;
  issueDate: string;
  expiryDate: string | null;
  credentialUrl: string;
  isVerified: boolean;
}

export interface LiveSession {
  id: string;
  teacherId: string;
  teacher: Teacher;
  title: string;
  description: string;
  sessionType: SessionType;
  language: string;
  scheduledStart: string;
  scheduledEnd: string;
  actualStart: string | null;
  actualEnd: string | null;
  status: SessionStatus;
  maxParticipants: number;
  currentParticipants: number;
  meetingUrl: string;
  recordingUrl: string;
  price: number;
}

export interface SessionParticipant {
  id: string;
  sessionId: string;
  childId: string;
  childName: string;
  childAvatar: string;
  status: ParticipantStatus;
  joinedAt: string | null;
  leftAt: string | null;
}

export interface SessionRating {
  id: string;
  sessionId: string;
  childId: string;
  parentId: string;
  rating: number;
  feedback: string;
  wouldRecommend: boolean;
}

export interface TeacherPerformanceMetrics {
  teacherId: string;
  month: string;
  sessionsConducted: number;
  totalStudents: number;
  averageRating: number;
  attendanceRate: number;
  earnings: number;
  complaints: number;
  positiveReviews: number;
}

export interface LiveSessionFilters {
  language?: string;
  sessionType?: SessionType;
  teacherId?: string;
  dateFrom?: string;
  dateTo?: string;
  priceMax?: number;
}

export interface LiveClassesState {
  upcomingSessions: LiveSession[];
  mySessions: LiveSession[];
  teachers: Teacher[];
  selectedSession: LiveSession | null;
  filters: LiveSessionFilters;
  isLoading: boolean;
  error: string | null;
}

export interface BookingRequest {
  sessionId: string;
  childId: string;
}

export interface BookingResponse {
  success: boolean;
  participantId: string;
  meetingUrl: string;
  confirmationCode: string;
}
