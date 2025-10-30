from django.db import models
from students.models import Student

class Hostel(models.Model):
    TYPE_CHOICES = ( ('boys', 'Boys'), ('girls', 'Girls') )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    total_rooms = models.IntegerField(blank=True, null=True)
    occupied_rooms = models.IntegerField(default=0)
    warden = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class HostelRoom(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
    )
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=10)
    capacity = models.IntegerField(default=1)
    occupied_beds = models.IntegerField(default=0)
    rent = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hostel.name} - Room {self.room_number}"

class HostelAllocation(models.Model):
    STATUS_CHOICES = ( ('active', 'Active'), ('checkout', 'Checkout') )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="hostel_allocation")
    room = models.ForeignKey(HostelRoom, on_delete=models.SET_NULL, null=True, related_name="allocations")
    allocation_date = models.DateField()
    checkout_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

class TransportRoute(models.Model):
    route_name = models.CharField(max_length=100)
    source = models.CharField(max_length=100, blank=True, null=True)
    destination = models.CharField(max_length=100, blank=True, null=True)
    distance = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    fare = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_contact = models.CharField(max_length=20, blank=True, null=True)
    vehicle_number = models.CharField(max_length=20, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.route_name

class TransportAssignment(models.Model):
    STATUS_CHOICES = ( ('active', 'Active'), ('inactive', 'Inactive') )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="transport_assignment")
    route = models.ForeignKey(TransportRoute, on_delete=models.SET_NULL, null=True, related_name="assignments")
    assignment_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)