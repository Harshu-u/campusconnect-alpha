from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timetable

# This is the main view for the 'courses' app, as listed in your roadmap
@login_required
def courses_view(request):
    # We will add dynamic data here in Phase 3
    context = {}
    return render(request, 'courses/courses.html', context)
@login_required
def timetable_view(request):
    # We will make this dynamic in Phase 3
    # For now, just pass the context needed by the template
    context = {
        'days_of_week': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    }
    # Render the existing template
    return render(request, 'core/timetable.html', context)

# add_course_view, edit_course_view, etc. will be added here later.