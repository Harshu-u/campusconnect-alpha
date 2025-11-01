# --- File: core/views.py ---
# This is the full and correct file.

from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# --- Import models for Dashboard ---
from students.models import Student, Department
from faculty.models import Faculty
from courses.models import Course
from attendance.models import Attendance
from timetable.models import Timetable
from library.models import BookIssue
from core.models import User
from django.db.models import Count, Case, When, FloatField
from datetime import date, timedelta
import json

# View for the public landing page
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')

# View for the dashboard (requires login)
@login_required
def dashboard_view(request):
    
    # --- 1. Top Stat Cards ---
    student_count = Student.objects.filter(status='active').count()
    faculty_count = Faculty.objects.filter(status='active').count()
    course_count = Course.objects.filter(is_active=True).count()

    total_records = Attendance.objects.count()
    present_records = Attendance.objects.filter(status__in=['present', 'late']).count()
    attendance_rate = 0.0
    if total_records > 0:
        attendance_rate = round((present_records / total_records) * 100, 1)

    # --- 2. Chart Data: Enrollment by Department ---
    dept_enrollment = Student.objects.filter(status='active') \
                                   .values('department__name') \
                                   .annotate(count=Count('id')) \
                                   .order_by('-count')
    
    # Convert to JSON for Chart.js
    dept_labels = json.dumps([item['department__name'] for item in dept_enrollment])
    dept_data = json.dumps([item['count'] for item in dept_enrollment])

    # --- 3. Chart Data: Weekly Attendance Trend ---
    today = date.today()
    attendance_trend_labels = []
    attendance_trend_data = []
    
    for i in range(6, -1, -1): # Loop for the last 7 days (today = 0)
        day = today - timedelta(days=i)
        attendance_trend_labels.append(day.strftime('%a, %b %d')) # e.g., "Sat, Nov 01"
        
        day_records = Attendance.objects.filter(date=day)
        day_total = day_records.count()
        day_present = day_records.filter(status__in=['present', 'late']).count()
        
        day_rate = 0.0
        if day_total > 0:
            day_rate = round((day_present / day_total) * 100, 1)
        attendance_trend_data.append(day_rate)

    # --- 4. Today's Schedule ---
    day_of_week = today.isoweekday() # Monday is 1, Sunday is 7
    todays_schedule = Timetable.objects.filter(day_of_week=day_of_week) \
                                     .select_related('course', 'faculty__user') \
                                     .order_by('start_time')

    # --- 5. Alerts & Quick Info ---
    pending_faculty = User.objects.filter(role='faculty', is_active=False).count()
    overdue_books = BookIssue.objects.filter(status='issued', due_date__lt=today).count()

    context = {
        'student_count': student_count,
        'faculty_count': faculty_count,
        'course_count': course_count,
        'attendance_rate': attendance_rate,
        'dept_enrollment_labels': dept_labels,
        'dept_enrollment_data': dept_data,
        'attendance_trend_labels': json.dumps(attendance_trend_labels),
        'attendance_trend_data': json.dumps(attendance_trend_data),
        'todays_schedule': todays_schedule,
        'pending_faculty_count': pending_faculty,
        'overdue_books_count': overdue_books,
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