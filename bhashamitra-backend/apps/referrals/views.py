"""Referral API views."""
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta

from .models import ReferralCode, Referral, AmbassadorProgram

logger = logging.getLogger(__name__)


class MyReferralCodeView(APIView):
    """Get or create the current user's referral code."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's referral code."""
        referral_code, created = ReferralCode.objects.get_or_create(
            user=request.user,
            defaults={
                'code': ReferralCode.generate_code(),
                'is_active': True,
            }
        )
        
        return Response({
            'code': referral_code.code,
            'share_url': f"{request.build_absolute_uri('/')[:-1] if request.build_absolute_uri('/').endswith('/') else request.build_absolute_uri('/')}join/{referral_code.code}",
            'total_referrals': referral_code.total_referrals,
            'successful_referrals': referral_code.successful_referrals,
            'total_earnings': float(referral_code.total_earnings),
        })


class ReferralStatsView(APIView):
    """Get referral statistics."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get referral stats."""
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
        except ReferralCode.DoesNotExist:
            return Response({
                'error': 'No referral code found'
            }, status=status.HTTP_404_NOT_FOUND)

        referrals = Referral.objects.filter(referral_code=referral_code)
        
        return Response({
            'total_referrals': referrals.count(),
            'pending': referrals.filter(status='PENDING').count(),
            'signed_up': referrals.filter(status='SIGNED_UP').count(),
            'in_trial': referrals.filter(status='TRIAL').count(),
            'converted': referrals.filter(status='CONVERTED').count(),
            'total_earnings': float(referral_code.total_earnings),
            'successful_referrals': referral_code.successful_referrals,
        })


class ReferralListView(APIView):
    """List user's referrals."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get list of referrals."""
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
        except ReferralCode.DoesNotExist:
            return Response({'referrals': []})

        referrals = Referral.objects.filter(
            referral_code=referral_code
        ).order_by('-created_at')[:50]
        
        data = [{
            'id': str(r.id),
            'email': r.referred_email or 'Pending signup',
            'status': r.status,
            'converted_at': r.converted_at,
            'reward_paid': float(r.reward_amount) if r.reward_paid_at else 0,
        } for r in referrals]
        
        return Response({'referrals': data})


class ApplyReferralCodeView(APIView):
    """
    Apply a referral code during registration.
    
    POST /api/v1/referrals/apply/
    Body: {"code": "REFERRAL_CODE"}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """Apply referral code."""
        code = request.data.get('code', '').strip().upper()
        
        if not code:
            return Response({
                'valid': False,
                'message': 'Please provide a referral code'
            })
        
        try:
            referral_code = ReferralCode.objects.get(
                code=code,
                is_active=True
            )
            
            # Check if referrer is valid
            if not referral_code.user.is_active:
                return Response({
                    'valid': False,
                    'message': 'This referral code is no longer valid'
                })
            
            return Response({
                'valid': True,
                'message': 'Referral code applied successfully!',
                'discount': {
                    'percentage': 10,
                    'duration_months': 12,
                    'description': '10% discount for 12 months on subscription'
                }
            })
            
        except ReferralCode.DoesNotExist:
            return Response({
                'valid': False,
                'message': 'Invalid referral code'
            })


class AmbassadorStatusView(APIView):
    """Get ambassador program status."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Check if user is in ambassador program."""
        try:
            ambassador = AmbassadorProgram.objects.get(
                user=request.user,
                is_active=True
            )
            return Response({
                'is_ambassador': True,
                'tier': ambassador.tier,
                'commission_rate': float(ambassador.commission_rate),
                'total_earnings': float(ambassador.total_earnings),
                'pending_payout': float(ambassador.pending_payout),
                'lifetime_referrals': ambassador.l,
                'benefits': ambassador.tier_benefits
            })
        except AmbassadorProgram.DoesNotExist:
            return Response({
                'is_ambassador': False,
                'message': 'Join our ambassador program to earn rewards!'
            })


class JoinAmbassadorView(APIView):
    """Join the ambassador program."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Join ambassador program."""
        # Check if already a member
        if AmbassadorProgram.objects.filter(
            user=request.user,
            is_active=True
        ).exists():
            return Response({
                'message': 'You are already an ambassador!'
            })
        
        # Create ambassador profile
        ambassador = AmbassadorProgram.objects.create(
            user=request.user,
            tier='BRONZE',
            commission_rate=10.00,
            is_active=True
        )
        
        return Response({
            'message': 'Welcome to the ambassador program!',
            'tier': ambassador.tier,
            'commission_rate': float(ambassador.commission_rate),
            'benefits': ambassador.tier_benefits
        })
