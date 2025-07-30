from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id_user', 'role', 'phone_number', 'first_name', 'last_name', 'email', 'username']
        read_only_fields = ['id_user']


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']
        read_only_fields = ['id_ride_event', 'created_at']

class RideSerializer(serializers.ModelSerializer):
    id_rider = CustomUserSerializer(read_only=True)
    id_driver = CustomUserSerializer(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    distance_to_pickup = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Ride
        fields = ['id_ride', 'status', 'id_rider', 'id_driver', 'pickup_latitude', 'pickup_longitude',
                  'dropoff_latitude', 'dropoff_longitude', 'pickup_time', 'todays_ride_events', 'distance_to_pickup']
        
        read_only_fields = ['id_ride']

    def get_todays_ride_events(self, obj):
        # If todays_ride_events is already prefetched, use it
        if hasattr(obj, 'todays_ride_events_prefetch'):
            return RideEventSerializer(obj.todays_ride_events_prefetch, many=True).data
        
        # Otherwise, filter events created in the last 24 hours
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        todays_events = obj.events.filter(created_at__gte=twenty_four_hours_ago)
        return RideEventSerializer(todays_events, many=True).data


class RideEventDetailSerializer(serializers.ModelSerializer):
    id_ride = RideSerializer(read_only=True)

    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'id_ride', 'description', 'created_at']
        read_only_fields = ['id_ride_event', 'created_at']