from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, PassengerViewSet, RiderViewSet
from users.auth_views import (
    RegisterView,
    VerifyPhoneView,
    VerifyEmailView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    AccountStatusView,
    AccountRecoveryView,
    DistrictListView,
)


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'passengers', PassengerViewSet, basename='passenger')
router.register(r'riders', RiderViewSet, basename='rider')

# Authentication and User Account System (UAS) endpoints
uas_patterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-phone/', VerifyPhoneView.as_view(), name='verify-phone'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('account/status/', AccountStatusView.as_view(), name='account-status'),
    path('account/recover/', AccountRecoveryView.as_view(), name='account-recover'),
    path('districts/', DistrictListView.as_view(), name='districts'),
]

urlpatterns = [
    path('uas/', include(uas_patterns)),
] + router.urls