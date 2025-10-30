from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# This is the main view for the 'courses' app, as listed in your roadmap
@login_required
def courses_view(request):
    # We will add dynamic data here in Phase 3
    context = {}
    return render(request, 'courses/courses.html', context)

# add_course_view, edit_course_view, etc. will be added here later.