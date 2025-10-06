"""
Utility functions for authentication, verification, and notifications.
"""
import secrets
import logging
from typing import Optional
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP code.

    Args:
        length: Length of the OTP code (default: 6)

    Returns:
        A string of random digits
    """
    return ''.join([str(secrets.randbelow(10)) for _ in range(length)])


def send_sms(phone_number: str, message: str) -> bool:
    """
    Send SMS using configured SMS provider.

    Currently a placeholder - implement with your SMS provider (Twilio, Africa's Talking, etc.)

    Args:
        phone_number: Recipient phone number
        message: SMS message content

    Returns:
        True if successful, False otherwise
    """
    # TODO: Implement SMS Email using a local SMS provider


    # For development: log the SMS instead of sending
    logger.info(f"SMS to {phone_number}: {message}")
    return True


def send_verification_email(email: str, code: str, user_name: str = "") -> bool:
    """
    Send verification email with OTP code.

    Args:
        email: Recipient email address
        code: Verification code
        user_name: User's name for personalization

    Returns:
        True if successful, False otherwise
    """
    try:
        subject = 'SafeBoda - Email Verification Code'

        # Create HTML email
        html_message = f"""
        <html>
            <body>
                <h2>Welcome to SafeBoda{', ' + user_name if user_name else ''}!</h2>
                <p>Your email verification code is:</p>
                <h1 style="color: #4CAF50; letter-spacing: 5px;">{code}</h1>
                <p>This code will expire in 10 minutes.</p>
                <p>If you didn't request this code, please ignore this email.</p>
                <br>
                <p>Best regards,<br>SafeBoda Team</p>
            </body>
        </html>
        """

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Verification email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Email sending failed to {email}: {e}")
        return False


def send_password_reset_email(email: str, token: str, user_name: str = "") -> bool:
    """
    Send password reset email with reset link.

    Args:
        email: Recipient email address
        token: Password reset token
        user_name: User's name for personalization

    Returns:
        True if successful, False otherwise
    """
    try:
        subject = 'SafeBoda - Password Reset Request'

        # In production, use your actual frontend URL
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

        html_message = f"""
        <html>
            <body>
                <h2>Password Reset Request{', ' + user_name if user_name else ''}</h2>
                <p>You requested to reset your password for your SafeBoda account.</p>
                <p>Click the link below to reset your password:</p>
                <p><a href="{reset_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
                <p>Or copy and paste this link into your browser:</p>
                <p>{reset_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't request this reset, please ignore this email.</p>
                <br>
                <p>Best regards,<br>SafeBoda Team</p>
            </body>
        </html>
        """

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Password reset email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Password reset email sending failed to {email}: {e}")
        return False


def send_sms_verification(phone_number: str, code: str) -> bool:
    """
    Send SMS verification code.

    Args:
        phone_number: Recipient phone number
        code: Verification code

    Returns:
        True if successful, False otherwise
    """
    message = f"Your SafeBoda verification code is: {code}. This code will expire in 10 minutes."
    return send_sms(phone_number, message)


def send_account_recovery_notification(email: str, phone_number: str) -> bool:
    """
    Send account recovery notification.

    Args:
        email: User's email address
        phone_number: User's phone number

    Returns:
        True if successful, False otherwise
    """
    try:
        subject = 'SafeBoda - Account Recovered'

        html_message = """
        <html>
            <body>
                <h2>Account Recovery Successful</h2>
                <p>Your SafeBoda account has been successfully recovered.</p>
                <p>You can now log in using your credentials.</p>
                <p>If you didn't request this recovery, please contact support immediately.</p>
                <br>
                <p>Best regards,<br>SafeBoda Team</p>
            </body>
        </html>
        """

        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        # Also send SMS notification
        sms_message = "Your SafeBoda account has been recovered. If you didn't request this, contact support."
        send_sms(phone_number, sms_message)

        return True

    except Exception as e:
        logger.error(f"Account recovery notification failed: {e}")
        return False
