# --- File: courses/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from students.models import Department
from faculty.models import Faculty
from .forms import CourseForm
from django.contrib import messages
from django.db.models import Q

@login_required
def course_list_view(request):
    """
    Display a list of all courses with filtering.
    """
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to view this page.")
        return redirect('dashboard') 

    course_query = Course.objects.select_related('department', 'faculty', 'faculty__user').all()
    departments = Department.objects.all()

    # --- Filtering Logic ---
    search_query = request.GET.get('search', '')
    dept_query = request.GET.get('department', '')
    semester_query = request.GET.get('semester', '')

    if search_query:
        course_query = course_query.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(faculty__user__first_name__icontains=search_query) |
            Q(faculty__user__last_name__icontains=search_query)
        )
    
    if dept_query:
        try:
            course_query = course_query.filter(department__id=int(dept_query))
        except (ValueError, TypeError):
            pass  # Ignore invalid/empty dept ID

    if semester_query:
        try:
            course_query = course_query.filter(semester=int(semester_query))
        except (ValueError, TypeError):
            pass # Ignore invalid/empty semester

    context = {
        'courses': course_query,
        'departments': departments,
        'search_query': search_query,
        'dept_query': dept_query,
        'semester_query': semester_query,
    }
    return render(request, 'courses/courses.html', context)

@login_required
def add_course_view(request):
    """
    Handle adding a new course.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add courses.")
        return redirect('courses:courses')
        
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course has been added successfully!")
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
    """
    Handle editing an existing course.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit courses.")
        return redirect('courses:courses')
    
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course has been updated successfully!")
            return redirect('courses:courses')
    else:
        form = CourseForm(instance=course)
        
    context = {
        'form': form,
        'form_title': f'Edit Course: {course.name}'
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def delete_course_view(request, pk):
    """
    Handle deleting a course.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete courses.")
        return redirect('courses:courses')
    
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        try:
            course.delete()
            messages.success(request, f'Course "{course.name}" has been deleted.')
        except IntegrityError:
            messages.error(request, f'Cannot delete "{course.name}". It may be linked to other records.')
        return redirect('courses:courses')
    else:
        return redirect('courses:courses')