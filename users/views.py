from django.shortcuts import render
from django.core.cache import cache
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User, Passenger, Rider
from users.serializers import UserSerializer, PassengerSerializer, RiderSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing User instances.
    Provides CRUD operations for users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class PassengerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Passenger instances.
    Provides CRUD operations for passenger profiles.
    """
    queryset = Passenger.objects.all()
    serializer_class = PassengerSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter passengers based on user permissions.
        Regular users can only see their own passenger profile.
        """
        if self.request.user.is_staff:
            return Passenger.objects.all()
        return Passenger.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associate the passenger with the current user.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Get the current user's passenger profile.
        """
        try:
            passenger = Passenger.objects.get(user=request.user)
            serializer = self.get_serializer(passenger)
            return Response(serializer.data)
        except Passenger.DoesNotExist:
            return Response(
                {'error': 'Passenger profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


class RiderViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Rider instances.
    Provides CRUD operations for rider profiles.
    """
    queryset = Rider.objects.all()
    serializer_class = RiderSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter riders based on user permissions.
        Regular users can only see their own rider profile.
        Staff can see all riders.
        """
        if self.request.user.is_staff:
            return Rider.objects.all()
        return Rider.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Associate the rider with the current user.
        """
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """
        Get the current user's rider profile.
        """
        try:
            rider = Rider.objects.get(user=request.user)
            serializer = self.get_serializer(rider)
            return Response(serializer.data)
        except Rider.DoesNotExist:
            return Response(
                {'error': 'Rider profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def available_riders(self, request):
        """
        Get all available riders for passengers to see.
        Uses Redis caching with 5-minute timeout.
        """
        cache_key = 'available_riders'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        available_riders = Rider.objects.filter(
            is_available=True, 
            verification_status='approved'
        )
        serializer = self.get_serializer(available_riders, many=True)
        
        # Cache for 5 minutes (300 seconds)
        cache.set(cache_key, serializer.data, 300)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def update_location(self, request, pk=None):
        """
        Update rider's current location.
        """
        rider = self.get_object()
        if rider.user != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        latitude = request.data.get('current_latitude')
        longitude = request.data.get('current_longitude')
        
        if latitude is not None:
            rider.current_latitude = latitude
        if longitude is not None:
            rider.current_longitude = longitude
            
        rider.save()
        
        # Clear available riders cache when location is updated
        cache.delete('available_riders')
        
        serializer = self.get_serializer(rider)
        return Response(serializer.data)


