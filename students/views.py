from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Student
# We will add forms here later

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

# We will add add_student_view, edit_student_view, etc. here
