# --- File: faculty/views.py ---
# This is the full and correct file (with django-filter)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty
from core.models import User
from students.models import Department
from .forms import FacultyForm
from .filters import FacultyFilter # <-- IMPORT OUR NEW FILTER
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, transaction

@login_required
def faculty_view(request):
    """
    Display a list of all faculty members with filtering.
    Only accessible to Admins and Faculty.
    """
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to view this page.")
        return redirect('dashboard') 
        
    faculty_query = Faculty.objects.select_related('user', 'department').all()
    
    # --- NEW: Use django-filter ---
    faculty_filter = FacultyFilter(request.GET, queryset=faculty_query)
    filtered_faculty = faculty_filter.qs
    # --- END: Use django-filter ---

    context = {
        'faculty_list': filtered_faculty,   # Pass the filtered list
        'filter_form': faculty_filter,    # Pass the entire filter instance
        'departments': Department.objects.all(), # Kept for consistency
    }
    return render(request, 'faculty/faculty.html', context)

@login_required
def add_faculty_view(request):
    """
    Handle adding a new faculty member.
    Only accessible to Admins.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add faculty.")
        return redirect('faculty')
        
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            if form.save() is not None:
                messages.success(request, "Faculty member has been added successfully!")
                return redirect('faculty')
            else:
                pass 
    else:
        form = FacultyForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Faculty'
    }
    return render(request, 'faculty/faculty_form.html', context)

@login_required
def edit_faculty_view(request, pk):
    """
    Handle editing an existing faculty member.
    Only accessible to Admins.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit faculty profiles.")
        return redirect('faculty')
    
    faculty = get_object_or_404(Faculty, pk=pk)
    
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
    """
    Handle deleting a faculty member and their associated user account.
    Only accessible to Admins.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete faculty.")
        return redirect('faculty')
    
    faculty = get_object_or_404(Faculty, pk=pk)
    
    if request.method == 'POST':
        try:
            user = faculty.user
            faculty.delete()
            user.delete()
            messages.success(request, f'Faculty {user.first_name} {user.last_name} and their account have been deleted.')
        except IntegrityError:
            messages.error(request, f'Cannot delete {user.first_name}. They may be linked to courses.')
        return redirect('faculty')
    else:
        return redirect('faculty')