# --- File: library/views.py ---
# This is the full and correct file.

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Book, BookIssue
from students.models import Student # For student-specific queries
from django.db.models import Q

@login_required
def library_view(request):
    
    # --- Get Filter values ---
    active_tab = request.GET.get('tab', 'books') # Default to books tab
    search_query = request.GET.get('search', '')
    category_query = request.GET.get('category', '')

    # --- Filter Books ---
    books_query = Book.objects.all()
    if search_query:
        books_query = books_query.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    if category_query:
        books_query = books_query.filter(category__icontains=category_query)
        
    # Get distinct categories for the filter dropdown
    categories = Book.objects.values_list('category', flat=True).distinct().exclude(category__isnull=True)

    # --- Filter Issues ---
    issues_query = BookIssue.objects.select_related(
        'book', 'student', 'student__user'
    )
    
    # If a student is logged in, only show their issues
    if request.user.role == 'student':
        try:
            student_profile = request.user.student_profile
            issues_query = issues_query.filter(student=student_profile)
        except Student.DoesNotExist:
            issues_query = BookIssue.objects.none() # Student profile doesn't exist
    
    context = {
        'active_tab': active_tab,
        'books': books_query,
        'issues': issues_query,
        'categories': categories,
        'search_query': search_query,
        'category_query': category_query,
    }
    return render(request, 'library/library.html', context)