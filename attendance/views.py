# --- File: attendance/views.py ---
# This is the full and correct file (with fix)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Attendance
from students.models import Student
from courses.models import Course
from django.db.models import Count, Case, When, FloatField

@login_required
def attendance_view(request):
    today = date.today()
    
    # --- Get Filter values ---
    date_query = request.GET.get('date', today.strftime('%Y-%m-%d'))
    course_query = request.GET.get('course', '')
    student_query = request.GET.get('student', '')

    # --- Fetch Data ---
    attendance_records = Attendance.objects.select_related(
        'student', 'student__user', 'course'
    ).filter(date=date_query)

    if course_query:
        try:
            attendance_records = attendance_records.filter(course__id=int(course_query))
        except (ValueError, TypeError):
            pass # Ignore invalid course ID

    if student_query:
        try:
            attendance_records = attendance_records.filter(student__id=int(student_query))
        except (ValueError, TypeError):
            pass # Ignore invalid student ID
            
    # --- FIX IS HERE: Added .order_by('course') ---
    attendance_records = attendance_records.order_by('course')

    # --- Get Dropdown Data ---
    courses = Course.objects.filter(is_active=True)
    students = Student.objects.select_related('user').filter(status='active')
    
    # --- Calculate Summary ---
    summary_base_query = Attendance.objects.all()
    summary_title = "Overall Attendance Summary"
    
    if student_query:
        try:
            summary_base_query = summary_base_query.filter(student__id=int(student_query))
            selected_student = students.get(id=int(student_query))
            summary_title = f"{selected_student.user.first_name}'s Summary"
        except (ValueError, TypeError, Student.DoesNotExist):
            pass # Use overall summary

    summary_stats = summary_base_query.aggregate(
        total=Count('id'),
        attended=Count(
            Case(When(status__in=['present', 'late'], then=1))
        )
    )

    overall_rate = 0.0
    if summary_stats['total'] > 0:
        overall_rate = round((summary_stats['attended'] / summary_stats['total']) * 100, 1)

    context = {
        'today_date': today.strftime('%Y-%m-%d'),
        'attendance_records': attendance_records,
        'courses': courses,
        'students': students,
        'date_query': date_query,
        'course_query': course_query,
        'student_query': student_query,
        'summary_title': summary_title,
        'overall_rate': overall_rate,
    }
    return render(request, 'attendance/attendance.html', context)