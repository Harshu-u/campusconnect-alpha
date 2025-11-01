# --- File: students/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Department
from core.models import User # Import the User model
from .forms import StudentForm 
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, transaction # For handling database errors
import csv # For reading CSV files
import io # For decoding the uploaded file

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


# --- NEW: CSV Import View for DEPARTMENTS ---

@login_required
@transaction.atomic
def import_departments_csv(request):
    # Only Admin can import departments
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to import departments.")
        return redirect('students')

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid .csv file.')
            return redirect('students')

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.DictReader(io_string)
            
            created_count = 0
            
            for row in reader:
                # Use get_or_create to avoid duplicates based on the 'code'
                _, created = Department.objects.get_or_create(
                    code=row['code'],
                    defaults={
                        'name': row['name'],
                        'head_of_department': row.get('head_of_department', ''),
                        'description': row.get('description', ''),
                    }
                )
                
                if created:
                    created_count += 1

            messages.success(request, f'Successfully imported {created_count} new departments.')

        except IntegrityError as e:
            messages.error(request, f'Database Error: {e}. A department with that code might already exist. No departments were imported.')
            transaction.set_rollback(True) # Rollback changes
        except KeyError as e:
            messages.error(request, f'CSV Error: Missing required column: {e}. No departments were imported.')
            transaction.set_rollback(True) # Rollback changes
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True) # Rollback changes
            
        return redirect('students')

    return redirect('students')

# --- CSV Import View for STUDENTS ---

@login_required
@transaction.atomic # This makes the whole import one single database transaction
def import_students_csv(request):
    # Only Admin and Faculty can import
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to import students.")
        return redirect('students')

    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        # Check if it's a CSV file
        if not csv_file or not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a valid .csv file.')
            return redirect('students')

        # Read the CSV file
        try:
            # Decode the file as text
            data_set = csv_file.read().decode('UTF-8')
            # Wrap in an in-memory text buffer
            io_string = io.StringIO(data_set)
            # Use DictReader to read rows as dictionaries
            reader = csv.DictReader(io_string)
            
            created_count = 0
            
            for row in reader:
                # 1. Get the Department object
                try:
                    # Match by name (case-insensitive)
                    department = Department.objects.get(name__iexact=row['department_name'])
                except Department.DoesNotExist:
                    messages.error(request, f"Department '{row['department_name']}' in CSV does not exist. Import departments first. No students were imported.")
                    # Abort the transaction
                    transaction.set_rollback(True)
                    return redirect('students')
                except KeyError:
                    messages.error(request, "CSV is missing the 'department_name' column. No students were imported.")
                    transaction.set_rollback(True)
                    return redirect('students')

                # 2. Create the User account
                # We set a default password. The user can change it later.
                default_password = row.get('student_id', 'password123')
                
                user, created_user = User.objects.get_or_create(
                    username=row['student_id'], # Use student_id as the unique username
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'role': 'student',
                        'is_active': True
                    }
                )
                
                if created_user:
                    user.set_password(default_password) # Set the password for new users
                    user.save()

                # 3. Create the Student profile (if it doesn't already exist)
                _, created_student = Student.objects.get_or_create(
                    user=user,
                    student_id=row['student_id'],
                    defaults={
                        'department': department,
                        'year': int(row['year']),
                        'semester': int(row['semester']),
                        'phone': row.get('phone', ''), # .get() handles optional columns
                        'address': row.get('address', ''),
                        'guardian_name': row.get('guardian_name', ''),
                    }
                )
                
                if created_student:
                    created_count += 1

            messages.success(request, f'Successfully imported {created_count} new students.')

        except IntegrityError as e:
            messages.error(request, f'Database Error: {e}. A student or user might already exist. No students were imported.')
            transaction.set_rollback(True) # Rollback changes
        except (KeyError, TypeError, ValueError) as e:
            messages.error(request, f'CSV Error: Check your columns. Missing or invalid data for: {e}. No students were imported.')
            transaction.set_rollback(True) # Rollback changes
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True) # Rollback changes
            
        return redirect('students')

    else:
        # If it's a GET request, just redirect
        return redirect('students')

