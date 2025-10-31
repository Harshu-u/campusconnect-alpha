# --- File: courses/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from students.models import Department  # Import Department for filtering
from .forms import CourseForm          # Import the new form
from django.contrib import messages
from django.db.models import Q          # For complex 'OR' searches
from django.http import HttpResponseForbidden

@login_required
def courses_view(request):
    # Fetch all courses to start
    courses_query = Course.objects.select_related('department').all()
    
    # --- Filtering Logic ---
    search_query = request.GET.get('search', '')
    dept_query = request.GET.get('department', '')
    year_query = request.GET.get('year', '')
    sem_query = request.GET.get('semester', '')

    if search_query:
        courses_query = courses_query.filter(
            Q(name__icontains=search_query) | 
            Q(course_code__icontains=search_query)
        )
    
    if dept_query:
        # Check if dept_query is a valid integer before filtering
        try:
            courses_query = courses_query.filter(department__id=int(dept_query))
        except (ValueError, TypeError):
            pass  # Ignore if dept_query is not a valid ID (e.g., "")
        
    if year_query:
        try:
            courses_query = courses_query.filter(year=int(year_query))
        except (ValueError, TypeError):
            pass
        
    if sem_query:
        try:
            courses_query = courses_query.filter(semester=int(sem_query))
        except (ValueError, TypeError):
            pass
        
    # --- End Filtering Logic ---

    # Get all departments for the dropdown
    departments = Department.objects.all()

    context = {
        'courses': courses_query,
        'departments': departments,
        'search_query': search_query,
        'dept_query': dept_query,
        'year_query': year_query,
        'sem_query': sem_query,
    }
    return render(request, 'courses/courses.html', context)

@login_required
def add_course_view(request):
    # Only Admin and Faculty can add courses
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to add courses.")
        return redirect('courses:courses')

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course has been added successfully!')
            return redirect('courses:courses')
    else:
        form = CourseForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Course'
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def edit_course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to edit courses.")
        return redirect('courses:courses')

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course has been updated successfully!')
            return redirect('courses:courses')
    else:
        form = CourseForm(instance=course)
        
    context = {
        'form': form,
        'form_title': f'Edit Course: {course.course_code}'
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def delete_course_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    
    # Only Admins can delete
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete courses.")
        return redirect('courses:courses')

    if request.method == 'POST':
        course.delete()
        messages.success(request, f'Course {course.name} has been deleted.')
        return redirect('courses:courses')
    else:
        # Prevent GET request to delete
        return redirect('courses:courses')