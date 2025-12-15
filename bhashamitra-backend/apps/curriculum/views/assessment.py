"""Assessment and certificate views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.children.models import Child
from apps.curriculum.models.assessment import Assessment, AssessmentAttempt, Certificate
from apps.curriculum.serializers.assessment import (
    AssessmentSerializer,
    AssessmentDetailSerializer,
    AssessmentAttemptSerializer,
    AssessmentAttemptDetailSerializer,
    CertificateSerializer,
    CertificateDetailSerializer,
)
from apps.curriculum.services.assessment_service import AssessmentService


class AssessmentListView(APIView):
    """List available assessments."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)
        assessments = AssessmentService.get_available_assessments(child, language)

        return Response({'data': assessments})


class AssessmentDetailView(APIView):
    """Get assessment details."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            assessment = Assessment.objects.prefetch_related('questions').get(pk=pk)
        except Assessment.DoesNotExist:
            return Response({'detail': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssessmentSerializer(assessment)
        data = serializer.data

        # Check eligibility
        can_take, reason = AssessmentService.can_take_assessment(child, assessment)
        data['can_take'] = can_take
        data['reason'] = reason if not can_take else None

        # Get attempts
        attempts = AssessmentAttempt.objects.filter(
            child=child, assessment=assessment
        ).order_by('-started_at')[:5]
        data['recent_attempts'] = AssessmentAttemptSerializer(attempts, many=True).data

        return Response({'data': data})


class AssessmentStartView(APIView):
    """Start an assessment."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            assessment = Assessment.objects.get(pk=pk)
        except Assessment.DoesNotExist:
            return Response({'detail': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check eligibility
        can_take, reason = AssessmentService.can_take_assessment(child, assessment)
        if not can_take:
            return Response({'detail': reason}, status=status.HTTP_403_FORBIDDEN)

        # Start the assessment
        attempt = AssessmentService.start_assessment(child, assessment)

        # Get questions (without answers)
        from apps.curriculum.serializers.assessment import AssessmentQuestionSerializer
        questions = assessment.questions.all()
        if assessment.randomize_questions:
            questions = questions.order_by('?')[:assessment.questions_count]

        questions_data = AssessmentQuestionSerializer(questions, many=True).data

        return Response({
            'data': {
                'attempt_id': str(attempt.id),
                'assessment_name': assessment.name,
                'time_limit_minutes': assessment.time_limit_minutes,
                'passing_score': assessment.passing_score,
                'questions': questions_data,
            }
        }, status=status.HTTP_201_CREATED)


class AssessmentSubmitView(APIView):
    """Submit assessment answers."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        attempt_id = request.data.get('attempt_id')
        answers = request.data.get('answers', {})

        if not attempt_id:
            return Response(
                {'detail': 'attempt_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            attempt = AssessmentAttempt.objects.get(
                pk=attempt_id,
                child=child,
                assessment_id=pk
            )
        except AssessmentAttempt.DoesNotExist:
            return Response({'detail': 'Attempt not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if already completed
        if attempt.completed_at:
            return Response(
                {'detail': 'Assessment already submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Submit and grade
        result = AssessmentService.submit_assessment(attempt, answers)

        return Response({'data': result})


class AssessmentAttemptsView(APIView):
    """Get assessment attempts history."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language', child.language)
        attempts = AssessmentService.get_assessment_history(child, language)
        serializer = AssessmentAttemptSerializer(attempts, many=True)

        return Response({'data': serializer.data})


class AttemptDetailView(APIView):
    """Get detailed attempt results."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id, pk):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            attempt = AssessmentAttempt.objects.select_related('assessment').get(
                pk=pk, child=child
            )
        except AssessmentAttempt.DoesNotExist:
            return Response({'detail': 'Attempt not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AssessmentAttemptDetailSerializer(attempt)
        return Response({'data': serializer.data})


class CertificateListView(APIView):
    """Get certificates for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        language = request.query_params.get('language')
        certificates = AssessmentService.get_certificates(child, language)
        serializer = CertificateSerializer(certificates, many=True)

        return Response({'data': serializer.data})


class CertificateDetailView(APIView):
    """Get or verify a certificate."""
    permission_classes = [AllowAny]  # Allow public verification

    def get(self, request, child_id, certificate_id):
        """Get certificate details or verify by ID."""
        # If child_id is 'verify', this is a public verification
        if child_id == 'verify':
            result = AssessmentService.verify_certificate(certificate_id)
            return Response({'data': result})

        # Otherwise, require authentication
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        try:
            certificate = Certificate.objects.select_related(
                'assessment_attempt__assessment'
            ).get(certificate_id=certificate_id, child=child)
        except Certificate.DoesNotExist:
            return Response({'detail': 'Certificate not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CertificateDetailSerializer(certificate)
        return Response({'data': serializer.data})
