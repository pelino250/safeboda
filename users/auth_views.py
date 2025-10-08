"""
Authentication views for user registration, verification, and password management.
"""
from drf_spectacular.utils import extend_schema
from rest_framework import status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction

from users.models import User, VerificationCode, PasswordResetToken, District
from users.auth_serializers import (
    UserRegistrationSerializer,
    PhoneVerificationSerializer,
    EmailVerificationSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    AccountStatusSerializer,
    AccountRecoverySerializer,
    DistrictSerializer,
)
from users.utils import (
    send_verification_email,
    send_sms_verification,
    send_password_reset_email,
    send_account_recovery_notification,
)


class RegisterView(APIView):
    """
    User registration endpoint.
    """
    permission_classes = [permissions.AllowAny]
    @extend_schema(request=UserRegistrationSerializer, responses={201: UserRegistrationSerializer}, description="Register a new user")
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                user = serializer.save()

                # Generate and send verification codes
                phone_code = VerificationCode.generate_code(user, 'phone')
                email_code = VerificationCode.generate_code(user, 'email')

                # Send verification notifications
                send_sms_verification(user.phone_number, phone_code.code)
                send_verification_email(user.email, email_code.code, user.first_name)

            return Response({
                'message': 'Registration successful. Verification codes sent to your phone and email.',
                'user_id': user.id,
                'email': user.email,
                'phone_number': user.phone_number
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneView(APIView):
    """
    Phone verification endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PhoneVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Find valid verification code
        verification = VerificationCode.objects.filter(
            user=user,
            code=code,
            verification_type='phone',
            is_used=False
        ).order_by('-created_at').first()

        if not verification:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verification.is_valid():
            return Response({'error': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark code as used and verify phone
        verification.is_used = True
        verification.save()

        user.phone_verified = True

        # Activate account if both phone and email are verified
        if user.email_verified:
            user.is_active = True

        user.save()

        return Response({
            'message': 'Phone verified successfully.',
            'phone_verified': True,
            'email_verified': user.email_verified,
            'is_active': user.is_active
        }, status=status.HTTP_200_OK)


class VerifyEmailView(APIView):
    """
    Email verification endpoint.
    """
    permission_classes = [permissions.AllowAny]
    @extend_schema(request=EmailVerificationSerializer, responses={201: EmailVerificationSerializer}, description="Verify email")
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Find valid verification code
        verification = VerificationCode.objects.filter(
            user=user,
            code=code,
            verification_type='email',
            is_used=False
        ).order_by('-created_at').first()

        if not verification:
            return Response({'error': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)

        if not verification.is_valid():
            return Response({'error': 'Verification code has expired.'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark code as used and verify email
        verification.is_used = True
        verification.save()

        user.email_verified = True

        # Activate account if both phone and email are verified
        if user.phone_verified:
            user.is_active = True

        user.save()

        return Response({
            'message': 'Email verified successfully.',
            'email_verified': True,
            'phone_verified': user.phone_verified,
            'is_active': user.is_active
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    Password reset request endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success even if user not found (security best practice)
            return Response({
                'message': 'If an account with this email exists, a password reset link has been sent.'
            }, status=status.HTTP_200_OK)

        # Generate reset token
        reset_token = PasswordResetToken.generate_token(user)

        # Send reset email
        send_password_reset_email(user.email, reset_token.token, user.first_name)

        return Response({
            'message': 'If an account with this email exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Password reset confirmation endpoint.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token_string = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            reset_token = PasswordResetToken.objects.get(token=token_string)
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid reset token.'}, status=status.HTTP_400_BAD_REQUEST)

        if not reset_token.is_valid():
            return Response({'error': 'Reset token has expired or already been used.'}, status=status.HTTP_400_BAD_REQUEST)

        # Reset password
        user = reset_token.user
        user.set_password(new_password)

        # Unlock account if locked
        if user.is_account_locked:
            user.is_account_locked = False
            user.account_locked_until = None

        user.save()

        # Mark token as used
        reset_token.is_used = True
        reset_token.save()

        return Response({
            'message': 'Password reset successful. You can now log in with your new password.'
        }, status=status.HTTP_200_OK)


class AccountStatusView(APIView):
    """
    Account verification status endpoint.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = AccountStatusSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountRecoveryView(APIView):
    """
    Account recovery endpoint for locked accounts.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AccountRecoverySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']
        phone_number = serializer.validated_data['phone_number']

        try:
            user = User.objects.get(email=email, phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'No matching account found.'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_account_locked:
            return Response({'error': 'Account is not locked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Unlock account
        user.is_account_locked = False
        user.account_locked_until = None
        user.save()

        # Send notification
        send_account_recovery_notification(user.email, user.phone_number)

        return Response({
            'message': 'Account recovered successfully. You can now log in.'
        }, status=status.HTTP_200_OK)


class DistrictListView(generics.ListAPIView):
    """
    Rwanda districts list endpoint.
    """
    permission_classes = [permissions.AllowAny]
    queryset = District.objects.filter(is_active=True)
    serializer_class = DistrictSerializer
    pagination_class = None  # No pagination for districts
