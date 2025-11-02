from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TimetableSlot
from students.models import Department
from .forms import TimetableSlotForm
from django.contrib import messages
from collections import defaultdict

@login_required
def timetable_view(request):
    """
    Display the main timetable, filterable by department, year, and semester.
    """
    departments = Department.objects.all()
    
    # Get filter parameters
    selected_dept_id = request.GET.get('department')
    selected_year = request.GET.get('year', '1') # Default to 1st year
    selected_semester = request.GET.get('semester', '1') # Default to 1st semester

    timetable_slots = TimetableSlot.objects.none()
    timetable_grid = defaultdict(lambda: defaultdict(str))
    
    if selected_dept_id:
        try:
            # Fetch slots for the selected filter
            timetable_slots = TimetableSlot.objects.filter(
                department_id=selected_dept_id,
                year=selected_year,
                semester=selected_semester
            ).select_related('course', 'faculty__user')

            # --- This is the BERSERK part ---
            # We process the data into a grid structure for the template
            # This makes the template logic *incredibly* simple.
            
            # Define time slots (you can customize these)
            times = [
                "09:00 - 10:00", "10:00 - 11:00", "11:00 - 12:00", 
                "12:00 - 13:00", "13:00 - 14:00", "14:00 - 15:00", "15:00 - 16:00"
            ]
            days = TimetableSlot.DAY_CHOICES
            
            # Initialize grid
            grid = {time: {day[0]: None for day in days} for time in times}
            
            # Populate grid
            for slot in timetable_slots:
                time_key = f"{slot.start_time.strftime('%H:%M')} - {slot.end_time.strftime('%H:%M')}"
                if time_key in grid and slot.day_of_week in grid[time_key]:
                    grid[time_key][slot.day_of_week] = slot
            
            timetable_grid = grid

        except ValueError:
            messages.error(request, "Invalid filter options selected.")
            
    context = {
        'departments': departments,
        'timetable_grid': timetable_grid,
        'days': TimetableSlot.DAY_CHOICES,
        'times': timetable_grid.keys(),
        'selected_dept_id': selected_dept_id,
        'selected_year': selected_year,
        'selected_semester': selected_semester,
        'all_slots_list': timetable_slots # For an alternate "list" view
    }
    return render(request, 'timetable/timetable.html', context)

@login_required
def add_timetable_slot_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to modify the timetable.")
        return redirect('timetable')
        
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable slot added successfully.")
            # Redirect back to the same filtered view
            return redirect(f"{request.GET.get('next', '/timetable/')}?department={form.cleaned_data['department'].id}&year={form.cleaned_data['year']}&semester={form.cleaned_data['semester']}")
    else:
        form = TimetableSlotForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Timetable Slot'
    }
    return render(request, 'timetable/timetable_form.html', context)

@login_required
def edit_timetable_slot_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to modify the timetable.")
        return redirect('timetable')
        
    slot = get_object_or_404(TimetableSlot, pk=pk)
    
    if request.method == 'POST':
        form = TimetableSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            messages.success(request, "Timetable slot updated successfully.")
            return redirect(f"{request.GET.get('next', '/timetable/')}?department={form.cleaned_data['department'].id}&year={form.cleaned_data['year']}&semester={form.cleaned_data['semester']}")
    else:
        form = TimetableSlotForm(instance=slot)
        
    context = {
        'form': form,
        'form_title': 'Edit Timetable Slot'
    }
    return render(request, 'timetable/timetable_form.html', context)

@login_required
def delete_timetable_slot_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to modify the timetable.")
        return redirect('timetable')
        
    slot = get_object_or_404(TimetableSlot, pk=pk)
    
    if request.method == 'POST':
        dept_id = slot.department.id
        year = slot.year
        semester = slot.semester
        slot.delete()
        messages.success(request, "Timetable slot has been deleted.")
        return redirect(f"{request.GET.get('next', '/timetable/')}?department={dept_id}&year={year}&semester={semester}")
    else:
        return redirect('timetable')