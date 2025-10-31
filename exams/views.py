# --- File: exams/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Examination, ExamResult
from courses.models import Course
from students.models import Student

@login_required
def exams_view(request):
    
    # --- Get Filter values ---
    active_tab = request.GET.get('tab', 'exams') # Default to exams tab
    course_query = request.GET.get('course', '')
    exam_type_query = request.GET.get('exam_type', '')
    year_query = request.GET.get('year', '')
    
    # --- Fetch Data for Filters ---
    courses = Course.objects.filter(is_active=True)
    
    # --- Filter Examinations ---
    exams_query = Examination.objects.select_related('course').all()
    if course_query:
        try:
            exams_query = exams_query.filter(course__id=int(course_query))
        except (ValueError, TypeError):
            pass # Ignore invalid
            
    if exam_type_query:
        exams_query = exams_query.filter(exam_type=exam_type_query)
        
    if year_query:
        exams_query = exams_query.filter(academic_year=year_query)
        
    # --- Filter Results ---
    results_query = ExamResult.objects.select_related(
        'examination', 'student', 'student__user', 'examination__course'
    )
    
    # Apply the same filters to the results
    if course_query:
        try:
            results_query = results_query.filter(examination__course__id=int(course_query))
        except (ValueError, TypeError):
            pass
    
    if exam_type_query:
        results_query = results_query.filter(examination__exam_type=exam_type_query)
        
    if year_query:
        results_query = results_query.filter(examination__academic_year=year_query)
    
    # If a student is logged in, only show their results
    if request.user.role == 'student':
        try:
            student_profile = request.user.student_profile
            results_query = results_query.filter(student=student_profile)
        except Student.DoesNotExist:
            results_query = ExamResult.objects.none() # Student profile doesn't exist

    context = {
        'active_tab': active_tab,
        'examinations': exams_query,
        'results': results_query,
        'courses': courses,
        'course_query': course_query,
        'exam_type_query': exam_type_query,
        'year_query': year_query,
    }
    return render(request, 'exams/exams.html', context)