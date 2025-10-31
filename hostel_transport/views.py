# --- File: hostel_transport/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Hostel, HostelRoom, HostelAllocation, TransportRoute, TransportAssignment
from students.models import Student

@login_required
def hostel_view(request):
    
    active_tab = request.GET.get('tab', 'hostels') # Default to hostels
    
    # --- Fetch Data for all tabs ---
    hostels = Hostel.objects.all()
    rooms = HostelRoom.objects.select_related('hostel').order_by('hostel', 'room_number')
    allocations = HostelAllocation.objects.select_related(
        'student', 'student__user', 'room', 'room__hostel'
    )
    routes = TransportRoute.objects.all()
    assignments = TransportAssignment.objects.select_related(
        'student', 'student__user', 'route'
    )

    # --- Student-specific filtering ---
    if request.user.role == 'student':
        try:
            student_profile = request.user.student_profile
            allocations = allocations.filter(student=student_profile)
            assignments = assignments.filter(student=student_profile)
        except Student.DoesNotExist:
            allocations = HostelAllocation.objects.none()
            assignments = TransportAssignment.objects.none()

    context = {
        'active_tab': active_tab,
        'hostels': hostels,
        'rooms': rooms,
        'allocations': allocations,
        'routes': routes,
        'assignments': assignments,
    }
    return render(request, 'hostel_transport/hostel.html', context)