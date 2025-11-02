from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Exam, Result
from .forms import ExamForm, ResultForm
from students.models import Student
from courses.models import Course
from django.contrib import messages
from django.forms import modelformset_factory
from django.db import transaction

@login_required
def exam_list_view(request):
    """
    Display a list of all exams.
    """
    if request.user.role == 'student':
        # Students see their results
        results = Result.objects.filter(student__user=request.user).select_related('exam', 'exam__course').order_by('-exam__exam_date')
        return render(request, 'exams/student_results_view.html', {'results': results})
    
    # Faculty/Admin view
    exams = Exam.objects.select_related('course', 'course__department').order_by('-exam_date')
    
    context = {
        'exams': exams,
    }
    return render(request, 'exams/exam_list.html', context)


@login_required
def add_exam_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to create exams.")
        return redirect('exams')
        
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam created successfully.")
            return redirect('exams')
    else:
        form = ExamForm()
        
    context = {
        'form': form,
        'form_title': 'Create New Exam'
    }
    return render(request, 'exams/exam_form.html', context)

@login_required
def edit_exam_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit exams.")
        return redirect('exams')
        
    exam = get_object_or_404(Exam, pk=pk)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, "Exam updated successfully.")
            return redirect('exams')
    else:
        form = ExamForm(instance=exam)
        
    context = {
        'form': form,
        'form_title': f'Edit Exam: {exam.name}'
    }
    return render(request, 'exams/exam_form.html', context)

@login_required
def delete_exam_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to delete exams.")
        return redirect('exams')
        
    exam = get_object_or_404(Exam, pk=pk)
    
    if request.method == 'POST':
        exam.delete()
        messages.success(request, "Exam deleted successfully.")
        return redirect('exams')
    else:
        return redirect('exams')


@login_required
@transaction.atomic
def manage_results_view(request, exam_pk):
    """
    Manage results for all students for a specific exam.
    """
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to manage results.")
        return redirect('exams')
        
    exam = get_object_or_404(Exam, pk=exam_pk)
    
    # Get all students in the course's department and year
    # This is a simplification; a real system might have explicit course enrollment
    students = Student.objects.filter(
        department=exam.course.department,
        status='active'
        # You might add year/semester filter here
    ).select_related('user')
    
    # Create a list of initial data for the formset
    initial_data = []
    student_result_map = {result.student_id: result for result in exam.results.all()}

    for student in students:
        result = student_result_map.get(student.id)
        initial_data.append({
            'student_id': student.id,
            'student_name': student.user.get_full_name(),
            'student_reg_id': student.student_id,
            'marks_obtained': result.marks_obtained if result else None,
        })

    if request.method == 'POST':
        # Process the submitted marks
        try:
            for student in students:
                marks_str = request.POST.get(f'marks_{student.id}')
                
                if marks_str is not None and marks_str != '':
                    marks = int(marks_str)
                    
                    if marks > exam.max_marks:
                         messages.warning(request, f"Marks for {student.user.get_full_name()} ({marks}) cannot be greater than max marks ({exam.max_marks}). Skipping.")
                         continue
                    
                    # Update or create the result
                    Result.objects.update_or_create(
                        student=student,
                        exam=exam,
                        defaults={
                            'marks_obtained': marks,
                            # Add grading/pass-fail logic here if needed
                            'is_pass': marks >= (exam.max_marks / 2) # Simple pass logic
                        }
                    )
                elif marks_str == '':
                    # If marks are cleared, delete the result
                    Result.objects.filter(student=student, exam=exam).delete()
            
            messages.success(request, f"Results for {exam.name} saved successfully.")
            return redirect('exams')
            
        except Exception as e:
            messages.error(request, f"An error occurred while saving results: {e}")

    context = {
        'exam': exam,
        'student_results': initial_data,
    }
    return render(request, 'exams/manage_results_form.html', context)