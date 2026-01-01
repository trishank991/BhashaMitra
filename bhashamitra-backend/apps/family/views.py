"""Views for family API."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Family, CurriculumChallenge, CurriculumChallengeParticipant
from .serializers import (
    FamilySerializer, FamilyCreateSerializer, FamilyDetailSerializer,
    CurriculumChallengeSerializer, CurriculumChallengeCreateSerializer,
    CurriculumChallengeDetailSerializer,
    CurriculumChallengeParticipantSerializer,
    ChallengeSubmitAnswerSerializer,
)
from .services import FamilyService, CurriculumChallengeService


class FamilyCreateView(APIView):
    """Create a new family for the authenticated user."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Create a new family."""
        existing_family = FamilyService.get_family_for_user(request.user)
        if existing_family:
            return Response({
                'success': False,
                'error': 'You already have a family. Leave it first to create a new one.',
                'family': FamilySerializer(existing_family).data
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = FamilyCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        family = FamilyService.create_family_for_user(
            request.user,
            name=serializer.validated_data.get('name', '')
        )

        return Response({
            'success': True,
            'data': FamilySerializer(family).data,
            'message': 'Family created successfully!'
        }, status=status.HTTP_201_CREATED)


class FamilyDetailView(APIView):
    """Get details of the user's family."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get family details."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family yet.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = FamilyDetailSerializer(family)
        return Response({
            'success': True,
            'data': serializer.data
        })


class FamilyJoinView(APIView):
    """Join a family using an invite code."""
    permission_classes = [IsAuthenticated]

    def post(self, request, code):
        """Join family with invite code."""
        try:
            family = FamilyService.join_family_via_code(request.user, code)
        except ValueError as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'data': FamilySerializer(family).data,
            'message': f'Joined {family.name} successfully!'
        })


class FamilyInviteCodeView(APIView):
    """Manage family invite code."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get current invite code and validity."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'data': {
                'invite_code': family.invite_code,
                'expires_at': family.invite_code_expires_at,
                'is_valid': family.is_invite_code_valid(),
                'children_count': family.total_children
            }
        })

    def post(self, request):
        """Refresh the invite code."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        new_code = FamilyService.refresh_family_code(family)

        return Response({
            'success': True,
            'data': {
                'invite_code': new_code,
                'expires_at': family.invite_code_expires_at,
                'is_valid': True
            },
            'message': 'Invite code refreshed!'
        })


class FamilyChildrenView(APIView):
    """Manage children in family."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get list of children in family."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        from apps.children.serializers import ChildProfileSerializer
        children = family.get_children()
        serializer = ChildProfileSerializer(children, many=True)

        return Response({
            'success': True,
            'data': serializer.data
        })

    def post(self, request):
        """Add a child to family."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        child_id = request.data.get('child_id')
        if not child_id:
            return Response({
                'success': False,
                'error': 'child_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        from apps.children.models import Child
        try:
            child = Child.objects.get(id=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Child not found'
            }, status=status.HTTP_404_NOT_FOUND)

        added = FamilyService.add_child_to_family(family, child)
        
        if added:
            return Response({
                'success': True,
                'message': f'{child.name} added to family!'
            })
        else:
            return Response({
                'success': False,
                'error': f'{child.name} is already in the family'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        """Remove a child from family."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        child_id = request.data.get('child_id')
        if not child_id:
            return Response({
                'success': False,
                'error': 'child_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        from apps.children.models import Child
        try:
            child = Child.objects.get(id=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Child not found'
            }, status=status.HTTP_404_NOT_FOUND)

        removed = FamilyService.remove_child_from_family(family, child)
        
        if removed:
            return Response({
                'success': True,
                'message': f'{child.name} removed from family'
            })
        else:
            return Response({
                'success': False,
                'error': f'{child.name} is not in this family'
            }, status=status.HTTP_400_BAD_REQUEST)


class ChallengeListCreateView(APIView):
    """List and create curriculum challenges."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all challenges for user's family."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        status_filter = request.query_params.get('status')
        challenges = CurriculumChallenge.objects.filter(family=family)
        
        if status_filter:
            challenges = challenges.filter(status=status_filter.upper())
        
        challenges = challenges.order_by('-created_at')
        
        serializer = CurriculumChallengeSerializer(challenges, many=True)
        return Response({
            'success': True,
            'data': serializer.data,
            'count': challenges.count()
        })

    def post(self, request):
        """Create a new curriculum challenge."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = CurriculumChallengeCreateSerializer(
            data=request.data,
            context={'request': request, 'family': family}
        )
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        challenge = serializer.save()
        
        return Response({
            'success': True,
            'data': CurriculumChallengeSerializer(challenge).data,
            'message': 'Challenge created successfully!'
        }, status=status.HTTP_201_CREATED)


class ChallengeDetailView(APIView):
    """Get details of a specific challenge."""
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        """Get challenge details with progress."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        challenge = get_object_or_404(
            CurriculumChallenge,
            id=challenge_id,
            family=family
        )

        serializer = CurriculumChallengeDetailSerializer(challenge)
        return Response({
            'success': True,
            'data': serializer.data
        })


class ChallengeStartView(APIView):
    """Start a pending challenge."""
    permission_classes = [IsAuthenticated]

    def post(self, request, challenge_id):
        """Start a pending challenge."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        challenge = get_object_or_404(
            CurriculumChallenge,
            id=challenge_id,
            family=family
        )

        if challenge.status != CurriculumChallenge.Status.PENDING:
            return Response({
                'success': False,
                'error': 'Challenge cannot be started.'
            }, status=status.HTTP_400_BAD_REQUEST)

        started = CurriculumChallengeService.start_challenge(challenge)
        
        if started:
            return Response({
                'success': True,
                'message': 'Challenge started!',
                'data': CurriculumChallengeSerializer(challenge).data
            })
        else:
            return Response({
                'success': False,
                'error': 'Failed to start challenge'
            }, status=status.HTTP_400_BAD_REQUEST)


class ChallengeSubmitAnswerView(APIView):
    """Submit an answer to a challenge."""
    permission_classes = [IsAuthenticated]

    def post(self, request, challenge_id):
        """Submit answer for a challenge."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        challenge = get_object_or_404(
            CurriculumChallenge,
            id=challenge_id,
            family=family
        )

        serializer = ChallengeSubmitAnswerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({
                'success': False,
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        child_id = str(serializer.validated_data['child_id'])
        participant = CurriculumChallengeService.get_participant_progress(
            challenge, child_id
        )

        result = CurriculumChallengeService.evaluate_answer(
            challenge, participant, serializer.validated_data
        )

        if result['is_complete']:
            CurriculumChallengeService.calculate_winner(challenge)

        return Response({
            'success': True,
            'data': result
        })


class ChallengeResultsView(APIView):
    """Get challenge results and leaderboard."""
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        """Get challenge results."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        challenge = get_object_or_404(
            CurriculumChallenge,
            id=challenge_id,
            family=family
        )

        participants = challenge.participants.all().order_by('-accuracy_score', '-completed_count')
        serializer = CurriculumChallengeParticipantSerializer(participants, many=True)

        return Response({
            'success': True,
            'data': {
                'challenge': CurriculumChallengeSerializer(challenge).data,
                'participants': serializer.data,
            }
        })


class ChildActiveChallengesView(APIView):
    """Get active challenges for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        """Get active challenges for a specific child."""
        from apps.children.models import Child
        
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user
        )

        challenges = CurriculumChallengeService.get_active_challenges_for_child(child_id)
        serializer = CurriculumChallengeSerializer(challenges, many=True)

        return Response({
            'success': True,
            'data': serializer.data,
            'count': challenges.count()
        })


class ChallengeQuestionsView(APIView):
    """Get questions for a challenge."""
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        """Get questions for a challenge."""
        family = FamilyService.get_family_for_user(request.user)
        
        if not family:
            return Response({
                'success': False,
                'error': 'You do not have a family.'
            }, status=status.HTTP_404_NOT_FOUND)

        challenge = get_object_or_404(
            CurriculumChallenge,
            id=challenge_id,
            family=family
        )

        if not challenge.is_active():
            return Response({
                'success': False,
                'error': 'Challenge is not active'
            }, status=status.HTTP_400_BAD_REQUEST)

        child_id = request.query_params.get('child_id')
        if not child_id:
            return Response({
                'success': False,
                'error': 'child_id is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        questions = CurriculumChallengeService.generate_questions_for_challenge(
            challenge, child_id
        )

        participant = CurriculumChallengeService.get_participant_progress(challenge, child_id)
        progress = CurriculumChallengeParticipantSerializer(participant).data

        return Response({
            'success': True,
            'data': {
                'challenge': CurriculumChallengeSerializer(challenge).data,
                'questions': questions,
                'progress': progress
            }
        })


class FamilyInviteValidateView(APIView):
    """Validate and get info about a family invite code."""
    permission_classes = []

    def get(self, request, code):
        """Validate invite code and return family info."""
        try:
            family = Family.objects.get(invite_code=code.upper())
        except Family.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid or expired invite code'
            }, status=status.HTTP_404_NOT_FOUND)

        if not family.is_invite_code_valid():
            return Response({
                'success': False,
                'error': 'This invite code has expired'
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'success': True,
            'data': {
                'name': family.name,
                'member_count': family.total_children,
                'has_pending_challenge': family.challenges.filter(
                    status=CurriculumChallenge.Status.ACTIVE
                ).exists()
            }
        })
