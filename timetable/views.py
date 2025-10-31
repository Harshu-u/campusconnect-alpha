from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Timetable

@login_required
def timetable_view(request):
    # We will make this dynamic in Phase 3
    context = {
        'days_of_week': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    }
    # Render the new template from the 'timetable' app
    return render(request, 'timetable/timetable.html', context) 