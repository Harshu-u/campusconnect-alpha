from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
from .forms import StudentForm # 1. Import the new form

@login_required
def students_view(request):
    # Only Admin can view this page
    if not request.user.role == 'admin':
        return redirect('dashboard') # Or show an error page
        
    students = Student.objects.select_related('user', 'department').all()
    context = {
        'students': students
    }
    # Note the new template path
    return render(request, 'students/students.html', context)

# 2. Add the new view (Task 1.B)
@login_required
def add_student_view(request):
    # Only Admin can use this view
    if not request.user.role == 'admin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: Add a success message (optional)
            return redirect('students')
    else:
        form = StudentForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Student Profile'
    }
    # We'll create this new template next
    return render(request, 'students/student_form.html', context)

# We will add edit_student_view, etc. here later