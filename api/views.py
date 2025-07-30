from django.shortcuts import render
from django.db.models import Prefetch, Case, When, FloatField, Q
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import django_filters

from .models import CustomUser, Ride, RideEvent
from .serializers import CustomUserSerializer, RideSerializer, RideEventSerializer, RideEventDetailSerializer
from .permissions import IsAdminUser


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class RideFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    rider_email = django_filters.CharFilter(field_name='id_rider__email', lookup_expr='icontains')
    pickup_time = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Ride
        fields = ['status', 'rider_email', 'pickup_time']


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'distance_to_pickup']
    ordering = ['pickup_time']

    def get_queryset(self):
        twenty_four_hours_ago = timezone.now() - timedelta(hours=24)
        
        # Prefetch only today's ride events for performance
        todays_events_prefetch = Prefetch(
            'events',
            queryset=RideEvent.objects.filter(created_at__gte=twenty_four_hours_ago).order_by('created_at'),
            to_attr='todays_ride_events_prefetch'
        )

        queryset = Ride.objects.select_related(
            'id_rider', 'id_driver'
        ).prefetch_related(
            todays_events_prefetch,
            'events'
        )

        # Handle distance-based sorting if GPS coordinates are provided
        lat = self.request.query_params.get('lat')
        lon = self.request.query_params.get('lon')
        
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                
                # Calculate distance to pickup using Haversine formula
                queryset = queryset.extra(
                    select={
                        'distance_to_pickup': """
                            6371 * acos(
                                cos(radians(%s)) * cos(radians(pickup_latitude)) * 
                                cos(radians(pickup_longitude) - radians(%s)) + 
                                sin(radians(%s)) * sin(radians(pickup_latitude))
                            )
                        """
                    },
                    select_params=[lat, lon, lat]
                )
                
            except (ValueError, TypeError):
                raise ValueError("Invalid GPS coordinates provided for distance calculation.")

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        ordering = request.query_params.get('ordering', 'pickup_time')
        if ordering in ['distance_to_pickup', '-distance_to_pickup']:
            lat = request.query_params.get('lat')
            lon = request.query_params.get('lon')
            if not (lat and lon):
                return Response(
                    {'error': 'GPS coordinates (lat, lon) are required for distance-based sorting'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Apply ordering
        queryset = queryset.order_by(ordering, 'pickup_time')

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.select_related('id_ride').all()
    serializer_class = RideEventDetailSerializer
    permission_classes = [IsAdminUser]
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
