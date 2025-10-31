from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course 

@login_required
def courses_view(request):
    # We will add dynamic data here in Phase 3
    context = {}
    return render(request, 'courses/courses.html', context)