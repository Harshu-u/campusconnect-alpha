from django.db import models
from students.models import Student
from django.utils.translation import gettext_lazy as _

class Hostel(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Hostel Name"))
    capacity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_number = models.CharField(max_length=20, verbose_name=_("Room Number"))
    capacity = models.PositiveIntegerField(default=3)
    
    class Meta:
        unique_together = ('hostel', 'room_number')

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='hostel_allocation')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocations')
    date_allocated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.room}"

class TransportRoute(models.Model):
    route_name = models.CharField(max_length=255, verbose_name=_("Route Name"))
    bus_number = models.CharField(max_length=50, verbose_name=_("Bus Number"))
    driver_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.route_name} ({self.bus_number})"

class TransportAllocation(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='transport_allocation')
    route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, blank=True, related_name='allocations')
    date_allocated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.route}"