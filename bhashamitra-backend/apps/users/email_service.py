"""Email service for user authentication emails."""
import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


class EmailService:
    """Service for sending user-related emails."""

    # Get frontend URL from settings with fallback
    @staticmethod
    def get_frontend_url():
        return getattr(settings, 'FRONTEND_URL', 'https://bhashamitra.vercel.app')

    @staticmethod
    def get_from_email():
        return getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@bhashamitra.co.nz')

    @classmethod
    def send_verification_email(cls, user, token):
        """
        Send email verification email to user.

        Args:
            user: User instance
            token: EmailVerificationToken instance
        """
        frontend_url = cls.get_frontend_url()
        verification_url = f"{frontend_url}/verify-email?token={token.token}"

        context = {
            'user_name': user.name,
            'verification_url': verification_url,
            'app_name': 'BhashaMitra',
            'support_email': 'support@bhashamitra.co.nz',
            'expiry_hours': 24,
        }

        subject = 'Verify your BhashaMitra account'

        # Plain text fallback
        message = f"""
Hi {user.name}!

Welcome to BhashaMitra! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

If you didn't create an account with BhashaMitra, you can safely ignore this email.

Best regards,
The BhashaMitra Team
"""

        try:
            # Try to use HTML template if it exists
            html_message = render_to_string('emails/verify_email.html', context)
        except Exception:
            # Fallback to simple HTML
            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Verify your email</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #FF6B35;">🦜 BhashaMitra</h1>
    </div>

    <h2>Hi {user.name}!</h2>

    <p>Welcome to BhashaMitra! We're excited to have you join our language learning community.</p>

    <p>Please verify your email address by clicking the button below:</p>

    <div style="text-align: center; margin: 30px 0;">
        <a href="{verification_url}"
           style="background-color: #FF6B35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
            Verify Email Address
        </a>
    </div>

    <p style="color: #666; font-size: 14px;">This link will expire in 24 hours.</p>

    <p style="color: #666; font-size: 14px;">If you didn't create an account with BhashaMitra, you can safely ignore this email.</p>

    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

    <p style="color: #999; font-size: 12px; text-align: center;">
        &copy; BhashaMitra - Making Indian language learning fun for kids!<br>
        <a href="mailto:support@bhashamitra.co.nz" style="color: #FF6B35;">support@bhashamitra.co.nz</a>
    </p>
</body>
</html>
"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=cls.get_from_email(),
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Verification email sent to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send verification email to {user.email}: {str(e)}")
            return False

    @classmethod
    def send_password_reset_email(cls, user, token):
        """
        Send password reset email to user.

        Args:
            user: User instance
            token: PasswordResetToken instance
        """
        frontend_url = cls.get_frontend_url()
        reset_url = f"{frontend_url}/reset-password?token={token.token}"

        context = {
            'user_name': user.name,
            'reset_url': reset_url,
            'app_name': 'BhashaMitra',
            'support_email': 'support@bhashamitra.co.nz',
            'expiry_hours': 1,
        }

        subject = 'Reset your BhashaMitra password'

        # Plain text fallback
        message = f"""
Hi {user.name},

We received a request to reset your BhashaMitra password. Click the link below to set a new password:

{reset_url}

This link will expire in 1 hour for security reasons.

If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.

Best regards,
The BhashaMitra Team
"""

        try:
            html_message = render_to_string('emails/password_reset.html', context)
        except Exception:
            html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Reset your password</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #FF6B35;">🦜 BhashaMitra</h1>
    </div>

    <h2>Hi {user.name},</h2>

    <p>We received a request to reset your BhashaMitra password.</p>

    <p>Click the button below to set a new password:</p>

    <div style="text-align: center; margin: 30px 0;">
        <a href="{reset_url}"
           style="background-color: #FF6B35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
            Reset Password
        </a>
    </div>

    <p style="color: #666; font-size: 14px;">⚠️ This link will expire in <strong>1 hour</strong> for security reasons.</p>

    <p style="color: #666; font-size: 14px;">If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>

    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

    <p style="color: #999; font-size: 12px; text-align: center;">
        &copy; BhashaMitra - Making Indian language learning fun for kids!<br>
        <a href="mailto:support@bhashamitra.co.nz" style="color: #FF6B35;">support@bhashamitra.co.nz</a>
    </p>
</body>
</html>
"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=cls.get_from_email(),
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Password reset email sent to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send password reset email to {user.email}: {str(e)}")
            return False

    @classmethod
    def send_welcome_email(cls, user):
        """
        Send welcome email after successful registration/verification.

        Args:
            user: User instance
        """
        frontend_url = cls.get_frontend_url()

        subject = '🎉 Welcome to BhashaMitra!'

        message = f"""
Namaste {user.name}! 🙏

Welcome to BhashaMitra - where language learning becomes an adventure!

Your account is all set up and ready to go. Here's what you can do next:

1. Add your child's profile to personalize their learning experience
2. Explore stories, songs, and games in multiple Indian languages
3. Meet Peppi the parrot - your child's friendly language learning companion!

Languages available: Hindi, Tamil, Telugu, Gujarati, Punjabi, Malayalam, and Fiji Hindi

Start learning: {frontend_url}

Need help? We're here for you at support@bhashamitra.co.nz

Happy learning!
The BhashaMitra Team
"""

        html_message = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Welcome to BhashaMitra!</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #FF6B35;">🦜 BhashaMitra</h1>
    </div>

    <h2>Namaste {user.name}! 🙏</h2>

    <p>Welcome to <strong>BhashaMitra</strong> - where language learning becomes an adventure!</p>

    <div style="background-color: #FFF5F0; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #FF6B35; margin-top: 0;">🚀 Get Started</h3>
        <ol style="padding-left: 20px;">
            <li><strong>Add your child's profile</strong> to personalize their learning</li>
            <li><strong>Explore stories, songs, and games</strong> in multiple Indian languages</li>
            <li><strong>Meet Peppi the parrot</strong> - your child's friendly language companion!</li>
        </ol>
    </div>

    <div style="background-color: #F0F9FF; padding: 20px; border-radius: 10px; margin: 20px 0;">
        <h3 style="color: #0066CC; margin-top: 0;">🌍 Languages Available</h3>
        <p>Hindi • Tamil • Telugu • Gujarati • Punjabi • Malayalam • Fiji Hindi</p>
    </div>

    <div style="text-align: center; margin: 30px 0;">
        <a href="{frontend_url}"
           style="background-color: #FF6B35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
            Start Learning
        </a>
    </div>

    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">

    <p style="text-align: center;">Need help? We're here for you!</p>
    <p style="text-align: center;">
        <a href="mailto:support@bhashamitra.co.nz" style="color: #FF6B35;">support@bhashamitra.co.nz</a>
    </p>

    <p style="color: #999; font-size: 12px; text-align: center;">
        &copy; BhashaMitra - Making Indian language learning fun for kids!
    </p>
</body>
</html>
"""

        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=cls.get_from_email(),
                recipient_list=[user.email],
                html_message=html_message,
                fail_silently=False,
            )
            logger.info(f"Welcome email sent to {user.email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send welcome email to {user.email}: {str(e)}")
            return False
