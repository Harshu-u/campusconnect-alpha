from django.contrib import admin
from .models import Hostel, Room, HostelAllocation, TransportRoute, TransportAllocation

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'hostel', 'capacity')
    list_filter = ('hostel',)
    
    # --- THIS IS THE FIX ---
    # This field is required by HostelAllocationAdmin's autocomplete
    search_fields = ('room_number', 'hostel__name')
    # --- END FIX ---

@admin.register(HostelAllocation)
class HostelAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'date_allocated')
    list_filter = ('room__hostel',)
    search_fields = ('student__user__username', 'student__student_id', 'room__room_number')
    autocomplete_fields = ('student', 'room')

@admin.register(TransportRoute)
class TransportRouteAdmin(admin.ModelAdmin):
    list_display = ('route_name', 'bus_number', 'driver_name')
    search_fields = ('route_name', 'bus_number')

@admin.register(TransportAllocation)
class TransportAllocationAdmin(admin.ModelAdmin):
    list_display = ('student', 'route', 'date_allocated')
    list_filter = ('route',)
    search_fields = ('student__user__username', 'student__student_id', 'route__route_name')
    autocomplete_fields = ('student', 'route')