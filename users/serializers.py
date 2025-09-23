from rest_framework import serializers

from users.models import User, Passenger, Rider


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'user_type']


class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'user', 'passenger_id', 'preferred_payment_method', 
            'home_address', 'profile_picture', 'preferred_language', 
            'emergency_contact', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rider
        fields = [
            'id', 'user', 'profile_picture', 'license_number', 'license_picture',
            'id_number_picture', 'verification_status', 'verification_notes',
            'is_available', 'current_latitude', 'current_longitude', 
            'average_rating', 'total_rides', 'total_earnings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'average_rating', 'total_rides', 'total_earnings', 'created_at', 'updated_at']