from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Attendance
from students.models import Student
from courses.models import Course
from faculty.models import Faculty
from .forms import MassAttendanceForm, AttendanceRecordForm
from django.contrib import messages
from django.db import transaction
import datetime

@login_required
def attendance_dashboard_view(request):
    """
    Main dashboard for faculty to take attendance or for students to view theirs.
    """
    if request.user.role == 'faculty':
        return redirect('take_attendance')
    else:
        # Student view
        attendances = Attendance.objects.filter(student__user=request.user).order_by('-date')
        
        # Calculate overall attendance percentage
        total_classes = attendances.count()
        present_classes = attendances.filter(status='present').count()
        percentage = (present_classes / total_classes * 100) if total_classes > 0 else 0
        
        context = {
            'attendances': attendances,
            'total_classes': total_classes,
            'present_classes': present_classes,
            'percentage': round(percentage, 2),
        }
        return render(request, 'attendance/student_attendance_view.html', context)

@login_required
@transaction.atomic
def take_attendance_view(request):
    """
    A view for faculty to take attendance for a selected course and date.
    """
    if not request.user.role == 'faculty':
        messages.error(request, "You do not have permission to take attendance.")
        return redirect('dashboard')
    
    try:
        faculty = request.user.faculty_profile
    except Faculty.DoesNotExist:
        messages.error(request, "Your faculty profile is not set up.")
        return redirect('dashboard')

    students = Student.objects.none()
    course = None
    date = None

    if request.method == 'POST':
        form = MassAttendanceForm(request.POST, faculty=faculty)
        
        if 'load_students' in request.POST:
            # Faculty has selected a course and date, show the student list
            if form.is_valid():
                course = form.cleaned_data['course']
                date = form.cleaned_data['date']
                # Get students enrolled in this course's department and year
                students = Student.objects.filter(
                    department=course.department, 
                    status='active'
                    # You might need to filter by year/semester here too
                )
        
        elif 'save_attendance' in request.POST:
            # Faculty is saving the attendance data
            course_id = request.POST.get('course')
            date_str = request.POST.get('date')
            
            try:
                course = Course.objects.get(id=course_id)
                date = datetime.date.fromisoformat(date_str)
                
                # Re-load the students to be safe
                students = Student.objects.filter(department=course.department, status='active')

                for student in students:
                    status = request.POST.get(f'status_{student.id}')
                    if status:
                        # Update or create the attendance record
                        Attendance.objects.update_or_create(
                            student=student,
                            course=course,
                            date=date,
                            defaults={
                                'status': status,
                                'faculty': faculty
                            }
                        )
                
                messages.success(request, f"Attendance for {course.title} on {date} saved successfully!")
                return redirect('attendance_dashboard')
                
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")

    else:
        form = MassAttendanceForm(faculty=faculty)

    context = {
        'form': form,
        'students': students,
        'course': course,
        'date': date,
    }
    return render(request, 'attendance/take_attendance_form.html', context)