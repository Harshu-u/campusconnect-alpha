# --- File: faculty/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty
from .forms import FacultyForm
from students.models import Department # Import for filtering
from django.contrib import messages
from django.db.models import Q

@login_required
def faculty_view(request):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard')
        
    faculty_list_query = Faculty.objects.select_related('user', 'department').all()
    departments = Department.objects.all()

    # --- Filtering Logic ---
    search_query = request.GET.get('search', '')
    dept_query = request.GET.get('department', '')

    if search_query:
        faculty_list_query = faculty_list_query.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )
    
    if dept_query:
        try:
            faculty_list_query = faculty_list_query.filter(department__id=int(dept_query))
        except (ValueError, TypeError):
            pass # Ignore invalid/empty dept ID
            
    # --- End Filtering Logic ---

    context = {
        'faculty_list': faculty_list_query,
        'departments': departments,
        'search_query': search_query,
        'dept_query': dept_query,
    }
    return render(request, 'faculty/faculty.html', context)

@login_required
def add_faculty_view(request):
    # Only Admin can use this view
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add faculty.")
        return redirect('faculty')
        
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty has been added successfully!")
            return redirect('faculty')
    else:
        form = FacultyForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Faculty Profile'
    }
    return render(request, 'faculty/faculty_form.html', context)

@login_required
def edit_faculty_view(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    
    # Only Admin can edit
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit faculty.")
        return redirect('faculty')

    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty profile has been updated successfully!")
            return redirect('faculty')
    else:
        form = FacultyForm(instance=faculty)
        
    context = {
        'form': form,
        'form_title': f'Edit Profile: {faculty.user.first_name} {faculty.user.last_name}'
    }
    return render(request, 'faculty/faculty_form.html', context)

@login_required
def delete_faculty_view(request, pk):
    faculty = get_object_or_404(Faculty, pk=pk)
    
    # Only Admin can delete
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete faculty.")
        return redirect('faculty')
        
    if request.method == 'POST':
        # We must delete the associated User object as well
        user = faculty.user
        faculty.delete()
        user.delete()
        messages.success(request, f'Faculty {user.first_name} {user.last_name} and their account have been deleted.')
        return redirect('faculty')
    else:
        # Prevent GET request to delete
        return redirect('faculty')