/**
 * Multi-child family and sibling challenge types
 */

export interface Family {
  id: string;
  name: string;
  primaryParentId: string;
  memberIds: string[];
  familyCode: string;
  discountTier: number;
  totalChildren: number;
  collectivePoints: number;
  createdAt: string;
  updatedAt: string;
}

export interface FamilyLeaderboard {
  id: string;
  familyId: string;
  weekStart: string;
  totalPoints: number;
  totalTimeMinutes: number;
  storiesCompleted: number;
  childRankings: ChildRanking[];
  rank: number;
}

export interface ChildRanking {
  childId: string;
  childName: string;
  avatar: string;
  points: number;
  storiesRead: number;
  rank: number;
}

export type ChallengeType = 'POINTS' | 'STORIES' | 'TIME' | 'STREAK' | 'WORDS';

export type ChallengeStatus = 'ACTIVE' | 'COMPLETED' | 'CANCELLED';

export interface SiblingChallenge {
  id: string;
  familyId: string;
  title: string;
  challengeType: ChallengeType;
  status: ChallengeStatus;
  participantIds: string[];
  startDate: string;
  endDate: string;
  targetValue: number;
  participantProgress: Record<string, number>;
  winnerId: string | null;
  prizeDescription: string;
  createdAt: string;
}

export interface FamilyDiscount {
  childCount: number;
  discountPercent: number;
  monthlyPrice: number;
  savings: number;
}

export interface FamilyState {
  family: Family | null;
  leaderboard: FamilyLeaderboard | null;
  activeChallenges: SiblingChallenge[];
  isLoading: boolean;
  error: string | null;
}
