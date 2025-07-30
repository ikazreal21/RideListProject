from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=[
        ('rider', 'Rider'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    ], default='rider')
    phone_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)


class Ride(models.Model):
    CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Picked Up'),
        ('dropoff', 'Dropped Off'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
        ('no-show', 'No Show'),
        ('waiting', 'Waiting'),
        ('scheduled', 'Scheduled'),
        ('in-progress', 'In Progress'),
    ]

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=CHOICES, default='waiting')
    id_rider = models.ForeignKey(CustomUser, related_name='rides_as_rider', on_delete=models.CASCADE)
    id_driver = models.ForeignKey(CustomUser, related_name='rides_as_driver', on_delete=models.CASCADE)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    def __str__(self):
        return f"Ride {self.id_ride} from {self.pickup_latitude}, {self.pickup_longitude} to {self.dropoff_latitude}, {self.dropoff_longitude} - Status: {self.status}"
    
    class Meta:
        ordering = ['pickup_time']
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'
        unique_together = ('id_rider', 'id_driver', 'pickup_time')
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['pickup_time']),
            models.Index(fields=['id_rider', 'status']),
            models.Index(fields=['pickup_latitude', 'pickup_longitude']),
        ]


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, related_name='events', on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id_ride_event} for Ride {self.id_ride.id_ride} - {self.description}"
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Ride Event'
        verbose_name_plural = 'Ride Events'
        unique_together = ('id_ride', 'description', 'created_at')
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['id_ride', 'created_at']),
        ]
