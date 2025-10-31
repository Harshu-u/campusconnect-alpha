from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Faculty
from .forms import FacultyForm # 1. Import the new form

@login_required
def faculty_view(request):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard')
        
    faculty_list = Faculty.objects.select_related('user', 'department').all()
    context = {
        'faculty_list': faculty_list
    }
    return render(request, 'faculty/faculty.html', context)

# 2. Add the new view (Task 1.D)
@login_required
def add_faculty_view(request):
    # Only Admin can use this view
    if not request.user.role == 'admin':
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faculty')
    else:
        form = FacultyForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Faculty Profile'
    }
    # We will create this new template next
    return render(request, 'faculty/faculty_form.html', context)