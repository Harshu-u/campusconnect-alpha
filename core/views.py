# --- File: core/views.py ---
# This is the full and correct file.

from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages # Import messages

# --- Import models for Dashboard ---
from students.models import Student
from faculty.models import Faculty
from courses.models import Course
from attendance.models import Attendance
from django.db.models import Count, Case, When, FloatField
# --- End Dashboard Imports ---


# View for the public landing page
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')

# View for the dashboard (requires login)
@login_required
def dashboard_view(request):
    # --- Get Main Statistics ---
    student_count = Student.objects.count()
    faculty_count = Faculty.objects.count()
    course_count = Course.objects.count()

    # --- Calculate Attendance Rate ---
    # We count 'present' and 'late' as "attended"
    total_records = Attendance.objects.count()
    present_records = Attendance.objects.filter(status__in=['present', 'late']).count()
    
    attendance_rate = 0.0
    if total_records > 0:
        # Calculate percentage and round to 1 decimal place
        attendance_rate = round((present_records / total_records) * 100, 1)

    # We will make the charts dynamic in a future step!
    context = {
        'student_count': student_count,
        'faculty_count': faculty_count,
        'course_count': course_count,
        'attendance_rate': attendance_rate,
    } 
    return render(request, 'core/dashboard.html', context)

# View for registration (with APPROVAL LOGIC)
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Don't save to DB yet
            
            # --- NEW APPROVAL LOGIC ---
            if user.role == 'student':
                user.is_active = True  # Students are approved automatically
            elif user.role == 'faculty':
                user.is_active = False # Faculty MUST be approved by admin
            # --- END NEW LOGIC ---
            
            user.save() # Now save the user
            
            # TODO: Add logic here to create the associated Student/Faculty profile
            
            # Only log in if they are active (i.e., students)
            if user.is_active:
                login(request, user)
                messages.success(request, 'Your account has been created successfully!')
                return redirect('dashboard')
            else:
                # Send faculty to the login page with a message
                messages.info(request, 'Your faculty account has been created. It must be approved by an administrator before you can log in.')
                return redirect('login') 
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})