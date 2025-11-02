# --- File: students/views.py ---
# This is the full and correct file (with filter context FIX)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student, Department
from core.models import User # Import the User model
from .forms import StudentForm, DepartmentForm
from .filters import StudentFilter # <-- IMPORT OUR NEW FILTER
from django.contrib import messages
from django.db.models import Q
from django.db import IntegrityError, transaction # For handling database errors
import csv # For reading CSV files
import io # For decoding the uploaded file

@login_required
def students_view(request):
    """
    List, filter, and search students.
    """
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('dashboard') 
        
    students_query = Student.objects.select_related('user', 'department').filter(status='active')
    
    # --- NEW: Use django-filter ---
    student_filter = StudentFilter(request.GET, queryset=students_query)
    filtered_students = student_filter.qs
    # --- END: Use django-filter ---

    context = {
        'students': filtered_students,
        # === FIXED: Pass the entire filter INSTANCE, not just the .form ===
        'filter_form': student_filter, 
        'departments': Department.objects.all(),
    }
    return render(request, 'students/students.html', context)

#
# ... all other views (add_student, edit_student, etc.) remain unchanged ...
#

@login_required
def add_student_view(request):
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
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to edit student profiles.")
        return redirect('students')
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student profile has been updated successfully!")
            return redirect('students')
    else:
        form = StudentForm(instance=student)
    context = {
        'form': form,
        'form_title': f'Edit Profile: {student.user.first_name} {student.user.last_name}'
    }
    return render(request, 'students/student_form.html', context)

@login_required
def delete_student_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete students.")
        return redirect('students')
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, f'Student {user.first_name} {user.last_name} and their account have been deleted.')
        return redirect('students')
    else:
        return redirect('students')

@login_required
@transaction.atomic
def import_departments_csv(request):
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
            transaction.set_rollback(True)
        except KeyError as e:
            messages.error(request, f'CSV Error: Missing required column: {e}. No departments were imported.')
            transaction.set_rollback(True)
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True)
        return redirect('students')
    return redirect('students')

@login_required
@transaction.atomic
def import_students_csv(request):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to import students.")
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
                try:
                    department = Department.objects.get(name__iexact=row['department_name'])
                except Department.DoesNotExist:
                    messages.error(request, f"Department '{row['department_name']}' in CSV does not exist. Import departments first. No students were imported.")
                    transaction.set_rollback(True)
                    return redirect('students')
                except KeyError:
                    messages.error(request, "CSV is missing the 'department_name' column. No students were imported.")
                    transaction.set_rollback(True)
                    return redirect('students')
                default_password = row.get('student_id', 'password123')
                user, created_user = User.objects.get_or_create(
                    username=row['student_id'],
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'role': 'student',
                        'is_active': True
                    }
                )
                if created_user:
                    user.set_password(default_password)
                    user.save()
                _, created_student = Student.objects.get_or_create(
                    user=user,
                    student_id=row['student_id'],
                    defaults={
                        'department': department,
                        'year': int(row['year']),
                        'semester': int(row['semester']),
                        'phone': row.get('phone', ''),
                        'address': row.get('address', ''),
                        'guardian_name': row.get('guardian_name', ''),
                        'status': 'active'
                    }
                )
                if created_student:
                    created_count += 1
            messages.success(request, f'Successfully imported {created_count} new students.')
        except IntegrityError as e:
            messages.error(request, f'Database Error: {e}. A student or user might already exist. No students were imported.')
            transaction.set_rollback(True)
        except (KeyError, TypeError, ValueError) as e:
            messages.error(request, f'CSV Error: Check your columns. Missing or invalid data for: {e}. No students were imported.')
            transaction.set_rollback(True)
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True)
        return redirect('students')
    else:
        return redirect('students')

@login_required
def department_list_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to view this page.")
        return redirect('dashboard') 
    departments = Department.objects.all()
    context = {
        'departments': departments,
    }
    return render(request, 'students/department_list.html', context)

@login_required
def add_department_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add departments.")
        return redirect('departments')
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Department has been added successfully!")
            return redirect('departments')
    else:
        form = DepartmentForm()
    context = {
        'form': form,
        'form_title': 'Add New Department'
    }
    return render(request, 'students/department_form.html', context)

@login_required
def edit_department_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit departments.")
        return redirect('departments')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            messages.success(request, "Department has been updated successfully!")
            return redirect('departments')
    else:
        form = DepartmentForm(instance=department)
    context = {
        'form': form,
        'form_title': f'Edit Department: {department.name}'
    }
    return render(request, 'students/department_form.html', context)

@login_required
def delete_department_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete departments.")
        return redirect('departments')
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        try:
            if department.students.exists() or department.faculty_members.exists() or department.courses.exists():
                 messages.error(request, f'Cannot delete "{department.name}". It is still linked to students, faculty, or courses. Please reassign them first.')
            else:
                department.delete()
                messages.success(request, f'Department "{department.name}" has been deleted.')
        except IntegrityError:
            messages.error(request, f'Cannot delete "{department.name}". It is still in use.')
        return redirect('departments')
    else:
        return redirect('departments')