# --- File: sports/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SportsEquipment, SportsEquipmentIssue
from students.models import Student
from django.db.models import Q

@login_required
def sports_view(request):
    
    # --- Get Filter values ---
    active_tab = request.GET.get('tab', 'equipment') # Default to equipment
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')
    condition_query = request.GET.get('condition', '')

    # --- Filter Equipment ---
    equipment_query = SportsEquipment.objects.all()
    if search_query:
        equipment_query = equipment_query.filter(
            Q(name__icontains=search_query) |
            Q(category__icontains=search_query)
        )
    if category_query:
        equipment_query = equipment_query.filter(category__icontains=category_query)
        
    if condition_query:
        equipment_query = equipment_query.filter(condition=condition_query)
        
    # Get distinct categories/conditions for filter dropdowns
    categories = SportsEquipment.objects.values_list('category', flat=True).distinct().exclude(category__isnull=True)
    conditions = [choice[0] for choice in SportsEquipment.CONDITION_CHOICES]

    # --- Filter Issues ---
    issues_query = SportsEquipmentIssue.objects.select_related(
        'equipment', 'student', 'student__user'
    )
    
    # If a student is logged in, only show their issues
    if request.user.role == 'student':
        try:
            student_profile = request.user.student_profile
            issues_query = issues_query.filter(student=student_profile)
        except Student.DoesNotExist:
            issues_query = SportsEquipmentIssue.objects.none()
    
    context = {
        'active_tab': active_tab,
        'equipment': equipment_query,
        'issues': issues_query,
        'categories': categories,
        'conditions': conditions,
        'search_query': search_query,
        'category_query': category_query,
        'condition_query': condition_query,
    }
    return render(request, 'sports/sports.html', context)