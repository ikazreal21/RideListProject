from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'user_type', 'phone_number', 'first_name', 'last_name', 'email']
        read_only_fields = ['id', 'user_type']

class RideSerializer(serializers.ModelSerializer):
    id_rider = CustomUserSerializer(read_only=True)
    id_driver = CustomUserSerializer(read_only=True)

    class Meta:
        model = Ride
        fields = ['id_ride', 'status', 'id_rider', 'id_driver', 'pickup_latitude', 'pickup_longitude',
                  'dropoff_latitude', 'dropoff_longitude', 'pickup_time']
        read_only_fields = ['id_ride', 'status']


class RideEventSerializer(serializers.ModelSerializer):
    id_ride = RideSerializer(read_only=True)

    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'id_ride', 'description', 'created_at']
        read_only_fields = ['id_ride_event', 'created_at']