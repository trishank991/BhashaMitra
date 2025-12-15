"""Assessment service for tests and certificates."""
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from typing import Tuple, List, Optional
from apps.curriculum.models.assessment import (
    Assessment, AssessmentQuestion, AssessmentAttempt, Certificate
)
from apps.children.models import Child


class AssessmentService:
    """Service for managing assessments and certificates."""

    @staticmethod
    def can_take_assessment(child: Child, assessment: Assessment) -> Tuple[bool, str]:
        """
        Check if child is eligible to take an assessment.
        Returns (can_take: bool, reason: str).
        """
        # Check level requirement
        if assessment.required_level and child.level < assessment.required_level:
            return False, f"Requires level {assessment.required_level}. Current level: {child.level}"

        # Check prerequisite assessment
        if assessment.prerequisite_assessment:
            passed = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment.prerequisite_assessment,
                passed=True
            ).exists()
            if not passed:
                return False, f"Must pass '{assessment.prerequisite_assessment.name}' first"

        # Check retake policy
        if not assessment.allow_retake:
            existing = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment
            ).exists()
            if existing:
                return False, "This assessment can only be taken once"

        # Check cooldown period between retakes
        if assessment.retake_cooldown_hours > 0:
            cooldown_time = timezone.now() - timedelta(hours=assessment.retake_cooldown_hours)
            recent = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment,
                completed_at__gte=cooldown_time
            ).exists()
            if recent:
                return False, f"Must wait {assessment.retake_cooldown_hours} hours between attempts"

        return True, "Eligible"

    @staticmethod
    @transaction.atomic
    def start_assessment(child: Child, assessment: Assessment) -> AssessmentAttempt:
        """
        Start a new assessment attempt.
        Creates the attempt record and returns it.
        """
        questions = assessment.questions.all()

        if assessment.randomize_questions:
            questions = questions.order_by('?')[:assessment.questions_count]
        else:
            questions = questions[:assessment.questions_count]

        max_score = sum(q.points for q in questions)

        attempt = AssessmentAttempt.objects.create(
            child=child,
            assessment=assessment,
            max_score=max_score
        )

        return attempt

    @staticmethod
    @transaction.atomic
    def submit_assessment(attempt: AssessmentAttempt, answers: dict) -> dict:
        """
        Grade and submit an assessment.

        Args:
            attempt: The assessment attempt
            answers: Dict mapping question_id (str) to user's answer (str)

        Returns dict with results.
        """
        total_score = 0
        skill_scores = {}
        results = []

        for question in attempt.assessment.questions.all():
            q_id = str(question.id)
            user_answer = answers.get(q_id, "")
            result = question.check_answer(user_answer)

            results.append({
                'question_id': q_id,
                'user_answer': user_answer,
                'is_correct': result['is_correct'],
                'points': result['points'],
                'correct_answer': result['correct_answer'] if attempt.assessment.show_correct_answers else None,
                'explanation': result.get('explanation', '') if attempt.assessment.show_correct_answers else None,
            })

            total_score += result['points']

            # Track scores by skill
            skill = question.skill_tested
            if skill not in skill_scores:
                skill_scores[skill] = {
                    'correct': 0,
                    'total': 0,
                    'points': 0,
                    'max_points': 0
                }
            skill_scores[skill]['total'] += 1
            skill_scores[skill]['max_points'] += question.points
            if result['is_correct']:
                skill_scores[skill]['correct'] += 1
                skill_scores[skill]['points'] += result['points']

        # Calculate percentage
        percentage = (total_score / attempt.max_score * 100) if attempt.max_score else 0
        passed = percentage >= attempt.assessment.passing_score

        # Update attempt record
        attempt.score = total_score
        attempt.percentage = round(percentage, 1)
        attempt.passed = passed
        attempt.completed_at = timezone.now()
        attempt.time_taken_seconds = int((attempt.completed_at - attempt.started_at).total_seconds())
        attempt.answers = answers
        attempt.skill_breakdown = skill_scores
        attempt.save()

        # Award points to child
        if passed:
            points_earned = int(total_score * 0.5)  # 50% of score as points
            attempt.child.total_points += points_earned
            attempt.child.save(update_fields=['total_points'])

        # Generate certificate if passed level-up assessment
        certificate = None
        if passed and attempt.assessment.assessment_type == 'LEVEL_UP':
            certificate = AssessmentService.generate_certificate(attempt)
            # Level up the child
            if attempt.child.level < 5:
                attempt.child.level += 1
                attempt.child.save(update_fields=['level'])

        return {
            'attempt_id': str(attempt.id),
            'score': total_score,
            'max_score': attempt.max_score,
            'percentage': attempt.percentage,
            'passed': passed,
            'passing_score': attempt.assessment.passing_score,
            'time_taken_seconds': attempt.time_taken_seconds,
            'skill_breakdown': skill_scores,
            'certificate_id': certificate.certificate_id if certificate else None,
            'results': results if attempt.assessment.show_correct_answers else None,
        }

    @staticmethod
    def generate_certificate(attempt: AssessmentAttempt) -> Certificate:
        """Generate a certificate for a passed assessment."""
        cert_type = 'LEVEL' if attempt.assessment.assessment_type == 'LEVEL_UP' else 'MODULE'

        title = f"{attempt.assessment.language.title()} Level {attempt.assessment.level} Achievement"
        description = (
            f"Successfully completed {attempt.assessment.name} "
            f"with a score of {attempt.percentage}%"
        )

        return Certificate.objects.create(
            child=attempt.child,
            certificate_type=cert_type,
            title=title,
            description=description,
            language=attempt.assessment.language,
            level=attempt.assessment.level,
            assessment_attempt=attempt,
        )

    @staticmethod
    def get_available_assessments(child: Child, language: str) -> List[dict]:
        """
        Get list of assessments with availability status for a child.
        """
        assessments = Assessment.objects.filter(
            language=language,
            is_active=True
        ).order_by('level', 'name')

        results = []
        for assessment in assessments:
            can_take, reason = AssessmentService.can_take_assessment(child, assessment)

            # Get best attempt
            best_attempt = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment,
            ).order_by('-percentage').first()

            # Check if already passed
            already_passed = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment,
                passed=True
            ).exists()

            results.append({
                'id': str(assessment.id),
                'name': assessment.name,
                'description': assessment.description,
                'type': assessment.assessment_type,
                'level': assessment.level,
                'questions_count': assessment.questions_count,
                'time_limit_minutes': assessment.time_limit_minutes,
                'passing_score': assessment.passing_score,
                'can_take': can_take,
                'reason': reason if not can_take else None,
                'best_score': best_attempt.percentage if best_attempt else None,
                'attempts': AssessmentAttempt.objects.filter(
                    child=child, assessment=assessment
                ).count(),
                'already_passed': already_passed,
            })

        return results

    @staticmethod
    def get_assessment_history(child: Child, language: str = None) -> List[dict]:
        """Get assessment attempt history for a child."""
        attempts_qs = AssessmentAttempt.objects.filter(
            child=child
        ).select_related('assessment')

        if language:
            attempts_qs = attempts_qs.filter(assessment__language=language)

        return list(attempts_qs.order_by('-started_at')[:20])

    @staticmethod
    def get_certificates(child: Child, language: str = None) -> List[Certificate]:
        """Get all certificates for a child."""
        certs_qs = Certificate.objects.filter(child=child)

        if language:
            certs_qs = certs_qs.filter(language=language)

        return list(certs_qs.order_by('-issued_at'))

    @staticmethod
    def verify_certificate(certificate_id: str) -> Optional[dict]:
        """Verify a certificate by its ID."""
        try:
            cert = Certificate.objects.select_related('child').get(
                certificate_id=certificate_id
            )
            return {
                'valid': True,
                'certificate_id': cert.certificate_id,
                'child_name': cert.child.name,
                'title': cert.title,
                'description': cert.description,
                'language': cert.language,
                'level': cert.level,
                'issued_at': cert.issued_at.isoformat(),
            }
        except Certificate.DoesNotExist:
            return {'valid': False, 'message': 'Certificate not found'}
