from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet, PassengerViewSet, RiderViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'passengers', PassengerViewSet, basename='passenger')
router.register(r'riders', RiderViewSet, basename='rider')

urlpatterns = [
] + router.urls