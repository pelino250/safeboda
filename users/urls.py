from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

router = routers.DefaultRouter()
router.register(r'', UserViewSet)

urlpatterns = [
] + router.urls