# --- File: faculty/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty
from core.models import User # Import User
from .forms import FacultyForm
from students.models import Department # Import for filtering
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, transaction # For handling database errors
import csv # For reading CSV files
import io # For decoding the uploaded file

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

# --- NEW: CSV Import View for Faculty ---

@login_required
@transaction.atomic # This makes the whole import one single database transaction
def import_faculty_csv(request):
    # Only Admin can import
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to import faculty.")
        return redirect('faculty')

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid .csv file.')
            return redirect('faculty')

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            
            for row in reader:
                # 1. Get the Department object
                try:
                    department = Department.objects.get(name__iexact=row['department_name'])
                except Department.DoesNotExist:
                    messages.error(request, f"Department '{row['department_name']}' in CSV does not exist. No faculty were imported.")
                    transaction.set_rollback(True)
                    return redirect('faculty')
                except KeyError:
                    messages.error(request, "CSV is missing the 'department_name' column. No faculty were imported.")
                    transaction.set_rollback(True)
                    return redirect('faculty')

                # 2. Create the User account
                default_password = row.get('employee_id', 'password123')
                
                user, created_user = User.objects.get_or_create(
                    username=row['employee_id'], # Use employee_id as the unique username
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'role': 'faculty',
                        'is_active': True # Admin is importing, so we can assume they are pre-approved
                    }
                )
                
                if created_user:
                    user.set_password(default_password) # Set password for new users
                    user.save()

                # 3. Create the Faculty profile (if it doesn't already exist)
                _, created_faculty = Faculty.objects.get_or_create(
                    user=user,
                    employee_id=row['employee_id'],
                    defaults={
                        'department': department,
                        'designation': row.get('designation', ''),
                        'qualification': row.get('qualification', ''),
                        'phone': row.get('phone', ''),
                        'address': row.get('address', ''),
                        'status': 'active' # Default to active
                    }
                )
                
                if created_faculty:
                    created_count += 1

            messages.success(request, f'Successfully imported {created_count} new faculty members.')

        except IntegrityError as e:
            messages.error(request, f'Database Error: {e}. A faculty member or user might already exist. No faculty were imported.')
            transaction.set_rollback(True) # Rollback changes
        except (KeyError, TypeError, ValueError) as e:
            messages.error(request, f'CSV Error: Check your columns. Missing or invalid data for: {e}. No faculty were imported.')
            transaction.set_rollback(True) # Rollback changes
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True) # Rollback changes
            
        return redirect('faculty')

    else:
        # If it's a GET request, just redirect
        return redirect('faculty')
