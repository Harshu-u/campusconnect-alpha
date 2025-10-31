# --- File: timetable/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timetable
from students.models import Department
from collections import defaultdict

@login_required
def timetable_view(request):
    
    # --- Get Filter values ---
    # We'll set defaults for the initial view
    dept_query = request.GET.get('department', '1') # Default to first department
    year_query = request.GET.get('year', '1')       # Default to year 1
    sem_query = request.GET.get('semester', '1')    # Default to semester 1

    # --- Fetch Data ---
    timetable_query = Timetable.objects.select_related(
        'course', 'faculty', 'faculty__user'
    ).order_by('start_time')
    
    departments = Department.objects.all()
    selected_dept = None

    # Apply filters if they are provided and valid
    try:
        if dept_query:
            timetable_query = timetable_query.filter(course__department__id=int(dept_query))
            selected_dept = departments.get(id=int(dept_query))
        if year_query:
            timetable_query = timetable_query.filter(course__year=int(year_query))
        if sem_query:
            timetable_query = timetable_query.filter(course__semester=int(sem_query))
    except (ValueError, TypeError, Department.DoesNotExist):
        pass # Ignore bad filter values

    # --- Process data into a grid ---
    # defaultdict(list) creates a dict where each new key gets an empty list
    timetable_grid = defaultdict(list)
    
    # We only care about Monday (1) to Friday (5)
    days_of_week_map = {
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
    }

    for day_num, day_name in days_of_week_map.items():
        # Get all entries for this specific day from the filtered query
        day_entries = timetable_query.filter(day_of_week=day_num)
        timetable_grid[day_name] = day_entries

    context = {
        'timetable_data': timetable_grid,
        'departments': departments,
        'selected_dept_name': selected_dept.name if selected_dept else "N/A",
        'dept_query': dept_query,
        'year_query': year_query,
        'sem_query': sem_query,
    }
    return render(request, 'timetable/timetable.html', context)