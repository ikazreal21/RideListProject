from django.contrib import admin
from .models import CustomUser, Ride, RideEvent
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'username', 'email', 'role', 'first_name', 'last_name', 'phone_number')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('role',)



class RideAdmin(admin.ModelAdmin):
    list_display = ('id_ride', 'id_rider', 'id_driver', 'status', 'pickup_time')
    search_fields = ('id_rider__username', 'id_driver__username', 'status')
    list_filter = ('status',)
    date_hierarchy = 'pickup_time'
    ordering = ('-pickup_time',)


class RideEventAdmin(admin.ModelAdmin):
    list_display = ('id_ride_event', 'id_ride', 'description', 'created_at')
    search_fields = ('id_ride__id_rider__username', 'id_ride__id_driver__username', 'description')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ride, RideAdmin)
admin.site.register(RideEvent, RideEventAdmin)