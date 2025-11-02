from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Faculty
from students.models import Department
from .forms import FacultyForm
from .filters import FacultyFilter
from django.contrib import messages
from django.db import IntegrityError, transaction
from core.models import User
import csv
import io

@login_required
def faculty_view(request):
    """
    List, filter, and search faculty.
    """
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to view this page.")
        return redirect('dashboard') 
        
    faculty_query = Faculty.objects.select_related('user', 'department').filter(status='active')
    
    faculty_filter = FacultyFilter(request.GET, queryset=faculty_query)
    filtered_faculty = faculty_filter.qs

    context = {
        'faculty_list': filtered_faculty,
        'filter_form': faculty_filter, 
        'departments': Department.objects.all(),
    }
    return render(request, 'faculty/faculty.html', context)

@login_required
def add_faculty_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add faculty.")
        return redirect('faculty')
        
    if request.method == 'POST':
        form = FacultyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty member has been added successfully!")
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
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit faculty.")
        return redirect('faculty')
        
    faculty_member = get_object_or_404(Faculty, pk=pk)
    
    if request.method == 'POST':
        form = FacultyForm(request.POST, instance=faculty_member)
        if form.is_valid():
            form.save()
            messages.success(request, "Faculty profile has been updated successfully!")
            return redirect('faculty')
    else:
        form = FacultyForm(instance=faculty_member)
        
    context = {
        'form': form,
        'form_title': f'Edit Profile: {faculty_member.user.first_name} {faculty_member.user.last_name}'
    }
    return render(request, 'faculty/faculty_form.html', context)

@login_required
def delete_faculty_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete faculty.")
        return redirect('faculty')
        
    faculty_member = get_object_or_404(Faculty, pk=pk)
    
    if request.method == 'POST':
        user = faculty_member.user
        faculty_member.delete()
        user.delete() 
        messages.success(request, f'Faculty {user.first_name} {user.last_name} and their account have been deleted.')
        return redirect('faculty')
    else:
        # GET request or other methods are not allowed for deletion
        return redirect('faculty')

@login_required
@transaction.atomic
def import_faculty_csv(request):
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
                try:
                    department = Department.objects.get(name__iexact=row['department_name'])
                except Department.DoesNotExist:
                    messages.error(request, f"Department '{row['department_name']}' in CSV does not exist. Import departments first. No faculty were imported.")
                    transaction.set_rollback(True)
                    return redirect('faculty')
                except KeyError:
                    messages.error(request, "CSV is missing the 'department_name' column. No faculty were imported.")
                    transaction.set_rollback(True)
                    return redirect('faculty')
                
                default_password = row.get('faculty_id', 'password123')
                
                user, created_user = User.objects.get_or_create(
                    username=row['faculty_id'],
                    defaults={
                        'email': row['email'],
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'role': 'faculty',
                        'is_active': True
                    }
                )
                
                if created_user:
                    user.set_password(default_password)
                    user.save()
                
                _, created_faculty = Faculty.objects.get_or_create(
                    user=user,
                    faculty_id=row['faculty_id'],
                    defaults={
                        'department': department,
                        'designation': row['designation'],
                        'specialization': row.get('specialization', ''),
                        'phone': row.get('phone', ''),
                        'office_location': row.get('office_location', ''),
                        'status': 'active'
                    }
                )
                
                if created_faculty:
                    created_count += 1
                    
            messages.success(request, f'Successfully imported {created_count} new faculty members.')
            
        except IntegrityError as e:
            messages.error(request, f'Database Error: {e}. A faculty member or user might already exist. No faculty were imported.')
            transaction.set_rollback(True)
        except (KeyError, TypeError, ValueError) as e:
            messages.error(request, f'CSV Error: Check your columns. Missing or invalid data for: {e}. No faculty were imported.')
            transaction.set_rollback(True)
        except Exception as e:
            messages.error(request, f'An unexpected error occurred: {e}')
            transaction.set_rollback(True)
            
        return redirect('faculty')
    else:
        return redirect('faculty')