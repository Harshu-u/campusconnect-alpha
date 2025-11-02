from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FeePayment, FeeStructure
from .forms import FeePaymentForm, FeeStructureForm
from students.models import Student
from django.contrib import messages
from django.db.models import Sum

@login_required
def fees_dashboard_view(request):
    """
    Main fees dashboard.
    - Students see their own payment history.
    - Admins/Faculty see all payments and can search/filter.
    """
    if request.user.role == 'student':
        payments = FeePayment.objects.filter(student__user=request.user).order_by('-academic_year', '-semester')
        total_paid = payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
        total_due = payments.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_balance = total_due - total_paid
        
        context = {
            'payments': payments,
            'total_paid': total_paid,
            'total_due': total_due,
            'total_balance': total_balance,
        }
        return render(request, 'fees/student_fees_view.html', context)
    
    # Admin/Faculty View
    # Simple search by student ID or name
    query = request.GET.get('q', '')
    if query:
        payments = FeePayment.objects.filter(
            Q(student__student_id__icontains=query) |
            Q(student__user__first_name__icontains=query) |
            Q(student__user__last_name__icontains=query)
        ).select_related('student__user').order_by('-payment_date')
    else:
        payments = FeePayment.objects.all().select_related('student__user').order_by('-payment_date')
    
    context = {
        'payments': payments,
        'search_query': query,
    }
    return render(request, 'fees/admin_fees_dashboard.html', context)

@login_required
def fee_structure_list_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to view this page.")
        return redirect('fees')
    
    structures = FeeStructure.objects.select_related('department').order_by('department', 'year')
    context = {
        'structures': structures,
    }
    return render(request, 'fees/fee_structure_list.html', context)

@login_required
def add_fee_structure_view(request):
    if not request.user.role == 'admin':
        return redirect('fees')
    
    if request.method == 'POST':
        form = FeeStructureForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee structure created successfully.")
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm()
        
    context = {
        'form': form,
        'form_title': 'Add Fee Structure'
    }
    return render(request, 'fees/fee_structure_form.html', context)

@login_required
def edit_fee_structure_view(request, pk):
    if not request.user.role == 'admin':
        return redirect('fees')
    
    structure = get_object_or_404(FeeStructure, pk=pk)
    
    if request.method == 'POST':
        form = FeeStructureForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, "Fee structure updated successfully.")
            return redirect('fee_structure_list')
    else:
        form = FeeStructureForm(instance=structure)
        
    context = {
        'form': form,
        'form_title': 'Edit Fee Structure'
    }
    return render(request, 'fees/fee_structure_form.html', context)

@login_required
def add_payment_view(request, student_pk):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('fees')
        
    student = get_object_or_404(Student, pk=student_pk)
    
    if request.method == 'POST':
        form = FeePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.student = student
            payment.save()
            messages.success(request, f"Payment for {student.user.get_full_name()} added.")
            return redirect('fees')
    else:
        form = FeePaymentForm(initial={'student': student})
        
    context = {
        'form': form,
        'student': student,
        'form_title': f'Add Payment for {student.user.get_full_name()}'
    }
    return render(request, 'fees/fee_payment_form.html', context)

@login_required
def edit_payment_view(request, pk):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('fees')
        
    payment = get_object_or_404(FeePayment, pk=pk)
    student = payment.student
    
    if request.method == 'POST':
        form = FeePaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment record updated.")
            return redirect('fees')
    else:
        form = FeePaymentForm(instance=payment)
        
    context = {
        'form': form,
        'student': student,
        'form_title': f'Edit Payment for {student.user.get_full_name()}'
    }
    return render(request, 'fees/fee_payment_form.html', context)