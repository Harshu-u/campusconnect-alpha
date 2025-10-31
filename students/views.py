# --- File: students/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm 

@login_required
def students_view(request):
    # MODIFIED: Allow Admin AND Faculty to view this page
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard') 
        
    students = Student.objects.select_related('user', 'department').all()
    context = {
        'students': students
    }
    return render(request, 'students/students.html', context)

@login_required
def add_student_view(request):
    # MODIFIED: Allow Admin AND Faculty to add students
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('students')
    else:
        form = StudentForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Student Profile'
    }
    return render(request, 'students/student_form.html', context)