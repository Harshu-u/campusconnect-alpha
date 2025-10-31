# --- File: students/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Department
from .forms import StudentForm 
from django.contrib import messages
from django.db.models import Q

@login_required
def students_view(request):
    # MODIFIED: Allow Admin AND Faculty to view this page
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard') 
        
    students_query = Student.objects.select_related('user', 'department').all()
    departments = Department.objects.all()

    # --- Filtering Logic ---
    search_query = request.GET.get('search', '')
    dept_query = request.GET.get('department', '')
    year_query = request.GET.get('year', '')

    if search_query:
        students_query = students_query.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(student_id__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    if dept_query:
        try:
            students_query = students_query.filter(department__id=int(dept_query))
        except (ValueError, TypeError):
            pass  # Ignore invalid/empty dept ID
        
    if year_query:
        try:
            students_query = students_query.filter(year=int(year_query))
        except (ValueError, TypeError):
            pass # Ignore invalid/empty year
            
    # --- End Filtering Logic ---

    context = {
        'students': students_query,
        'departments': departments,
        'search_query': search_query,
        'dept_query': dept_query,
        'year_query': year_query,
    }
    return render(request, 'students/students.html', context)

@login_required
def add_student_view(request):
    # MODIFIED: Allow Admin AND Faculty to add students
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to add students.")
        return redirect('students')
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student has been added successfully!")
            return redirect('students')
    else:
        form = StudentForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Student Profile'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def edit_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Only Admin and Faculty can edit
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to edit student profiles.")
        return redirect('students')
    
    if request.method == 'POST':
        # We pass 'instance=student' to update the existing object
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student profile has been updated successfully!")
            return redirect('students')
    else:
        # Pre-populate the form with the student's existing data
        form = StudentForm(instance=student)
        
    context = {
        'form': form,
        'form_title': f'Edit Profile: {student.user.first_name} {student.user.last_name}'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def delete_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    
    # Only Admin can delete
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete students.")
        return redirect('students')
        
    if request.method == 'POST':
        # We must delete the associated User object as well
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, f'Student {user.first_name} {user.last_name} and their account have been deleted.')
        return redirect('students')
    else:
        # Prevent GET request to delete
        return redirect('students')