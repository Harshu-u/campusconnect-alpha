from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Hostel, Room, HostelAllocation, TransportRoute, TransportAllocation
from .forms import HostelForm, RoomForm, HostelAllocationForm, TransportRouteForm, TransportAllocationForm
from students.models import Student
from django.contrib import messages
from django.db import IntegrityError

# --- Hostel Views ---

@login_required
def hostel_dashboard_view(request):
    """
    Main hostel dashboard.
    - Students see their own allocation.
    - Admins/Faculty see all allocations and an allocation form.
    """
    if request.user.role == 'student':
        try:
            allocation = HostelAllocation.objects.get(student__user=request.user)
        except HostelAllocation.DoesNotExist:
            allocation = None
        context = {'allocation': allocation}
        return render(request, 'hostel_transport/student_hostel_view.html', context)
    
    # Admin/Faculty View
    allocations = HostelAllocation.objects.select_related('student__user', 'room__hostel').order_by('room__hostel', 'room__room_number')
    
    if request.method == 'POST':
        form = HostelAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Hostel allocated successfully.")
            return redirect('hostel_dashboard')
    else:
        form = HostelAllocationForm()
        
    context = {
        'form': form,
        'allocations': allocations,
    }
    return render(request, 'hostel_transport/hostel_dashboard.html', context)

@login_required
def manage_hostels_view(request):
    """
    Admin view to add/edit hostels and rooms.
    """
    if not request.user.role == 'admin':
        return redirect('hostel_dashboard')
    
    if 'add_hostel' in request.POST:
        hostel_form = HostelForm(request.POST)
        if hostel_form.is_valid():
            hostel_form.save()
            messages.success(request, "Hostel added successfully.")
            return redirect('manage_hostels')
    else:
        hostel_form = HostelForm()

    if 'add_room' in request.POST:
        room_form = RoomForm(request.POST)
        if room_form.is_valid():
            try:
                room_form.save()
                messages.success(request, "Room added successfully.")
            except IntegrityError:
                messages.error(request, "A room with that number already exists in that hostel.")
            return redirect('manage_hostels')
    else:
        room_form = RoomForm()

    hostels = Hostel.objects.all()
    rooms = Room.objects.select_related('hostel').order_by('hostel__name', 'room_number')
    
    context = {
        'hostel_form': hostel_form,
        'room_form': room_form,
        'hostels': hostels,
        'rooms': rooms,
    }
    return render(request, 'hostel_transport/manage_hostels.html', context)

@login_required
def add_room_view(request):
    # This view is now part of manage_hostels_view
    return redirect('manage_hostels')

@login_required
def allocate_hostel_view(request):
    # This view is now part of hostel_dashboard_view
    return redirect('hostel_dashboard')


# --- Transport Views ---

@login_required
def transport_dashboard_view(request):
    """
    Main transport dashboard.
    - Students see their own allocation.
    - Admins/Faculty see all allocations and an allocation form.
    """
    if request.user.role == 'student':
        try:
            allocation = TransportAllocation.objects.get(student__user=request.user)
        except TransportAllocation.DoesNotExist:
            allocation = None
        context = {'allocation': allocation}
        return render(request, 'hostel_transport/student_transport_view.html', context)
    
    # Admin/Faculty View
    allocations = TransportAllocation.objects.select_related('student__user', 'route').order_by('route__route_name')
    
    if request.method == 'POST':
        form = TransportAllocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transport allocated successfully.")
            return redirect('transport_dashboard')
    else:
        form = TransportAllocationForm()
        
    context = {
        'form': form,
        'allocations': allocations,
    }
    return render(request, 'hostel_transport/transport_dashboard.html', context)

@login_required
def manage_transport_view(request):
    """
    Admin view to add/edit transport routes.
    """
    if not request.user.role == 'admin':
        return redirect('transport_dashboard')
    
    if request.method == 'POST':
        form = TransportRouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Transport route added successfully.")
            return redirect('manage_transport')
    else:
        form = TransportRouteForm()
        
    routes = TransportRoute.objects.all().order_by('route_name')
    
    context = {
        'form': form,
        'routes': routes,
    }
    return render(request, 'hostel_transport/manage_transport.html', context)

@login_required
def allocate_transport_view(request):
    # This view is now part of transport_dashboard_view
    return redirect('transport_dashboard')