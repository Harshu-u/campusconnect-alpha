# --- File: fees/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FeeStructure, FeePayment
from students.models import Student
from django.db.models import Q

@login_required
def fees_view(request):
    
    # --- Get Filter values ---
    active_tab = request.GET.get('tab', 'payments') # Default to payments
    search_query = request.GET.get('search', '')
    status_query = request.GET.get('status', '')

    # --- Filter Payments ---
    payments_query = FeePayment.objects.select_related(
        'student', 'student__user', 'fee_structure'
    )
    
    if search_query:
        payments_query = payments_query.filter(
            Q(student__user__first_name__icontains=search_query) |
            Q(student__user__last_name__icontains=search_query) |
            Q(student__student_id__icontains=search_query) |
            Q(transaction_id__icontains=search_query)
        )
    
    if status_query:
        payments_query = payments_query.filter(status=status_query)

    # If a student is logged in, only show their payments
    if request.user.role == 'student':
        try:
            student_profile = request.user.student_profile
            payments_query = payments_query.filter(student=student_profile)
        except Student.DoesNotExist:
            payments_query = FeePayment.objects.none()

    # --- Get Fee Structures ---
    structures_query = FeeStructure.objects.select_related('department')

    context = {
        'active_tab': active_tab,
        'payments': payments_query,
        'structures': structures_query,
        'search_query': search_query,
        'status_query': status_query,
    }
    return render(request, 'fees/fees.html', context)