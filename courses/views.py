from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course
from .forms import CourseForm
from .filters import CourseFilter
from django.contrib import messages

@login_required
def courses_view(request):
    """
    List, filter, and search courses.
    """
    course_query = Course.objects.select_related('department', 'faculty__user').filter(status='active')
    
    course_filter = CourseFilter(request.GET, queryset=course_query)
    filtered_courses = course_filter.qs

    context = {
        'courses': filtered_courses,
        'filter_form': course_filter,
    }
    return render(request, 'courses/courses.html', context)

@login_required
def add_course_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add courses.")
        return redirect('courses')
        
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course has been added successfully!")
            return redirect('courses')
    else:
        form = CourseForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Course'
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def edit_course_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit courses.")
        return redirect('courses')
        
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course has been updated successfully!")
            return redirect('courses')
    else:
        form = CourseForm(instance=course)
        
    context = {
        'form': form,
        'form_title': f'Edit Course: {course.title}'
    }
    return render(request, 'courses/course_form.html', context)

@login_required
def delete_course_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete courses.")
        return redirect('courses')
        
    course = get_object_or_404(Course, pk=pk)
    
    if request.method == 'POST':
        try:
            course.delete()
            messages.success(request, f'Course "{course.title}" has been deleted.')
        except Exception as e:
            messages.error(request, f'Cannot delete this course, it might be in use. Error: {e}')
        return redirect('courses')
    else:
        return redirect('courses')