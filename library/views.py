from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, BookIssue
from .forms import BookForm, BookIssueForm
from students.models import Student
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import datetime

@login_required
def library_dashboard_view(request):
    """
    Main dashboard.
    - Students see their own issued books.
    - Admins/Faculty see all issued books and an issue form.
    """
    if request.user.role == 'student':
        issued_books = BookIssue.objects.filter(student__user=request.user, return_date__isnull=True).select_related('book', 'student')
        context = {
            'issued_books': issued_books,
        }
        return render(request, 'library/student_library_view.html', context)
    
    # Admin/Faculty View
    issued_books = BookIssue.objects.filter(return_date__isnull=True).select_related('book', 'student__user').order_by('due_date')
    
    # Book Issue Form
    if request.method == 'POST':
        form = BookIssueForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            book = form.cleaned_data['book']
            
            # Berserk check: Is the book available?
            if book.available_copies <= 0:
                messages.error(request, f"'{book.title}' is not available (0 copies).")
            else:
                issue = form.save()
                # Decrement available copies
                book.available_copies -= 1
                book.save()
                messages.success(request, f"'{book.title}' issued to {student.user.get_full_name()} successfully.")
                return redirect('library')
    else:
        form = BookIssueForm()
        
    context = {
        'form': form,
        'issued_books': issued_books,
    }
    return render(request, 'library/library_dashboard.html', context)


@login_required
def book_list_view(request):
    """
    List all books, with search.
    """
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        return redirect('library')

    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | 
            Q(author__icontains=query) | 
            Q(isbn__icontains=query)
        ).order_by('title')
    else:
        books = Book.objects.all().order_by('title')
        
    context = {
        'books': books,
        'search_query': query,
    }
    return render(request, 'library/book_list.html', context)

@login_required
def add_book_view(request):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to add books.")
        return redirect('book_list')
        
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Book added successfully.")
            return redirect('book_list')
    else:
        form = BookForm()
        
    context = {
        'form': form,
        'form_title': 'Add New Book'
    }
    return render(request, 'library/book_form.html', context)

@login_required
def edit_book_view(request, pk):
    if not request.user.role == 'admin':
        messages.error(request, "You do not have permission to edit books.")
        return redirect('book_list')
        
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully.")
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
        
    context = {
        'form': form,
        'form_title': f'Edit Book: {book.title}'
    }
    return render(request, 'library/book_form.html', context)

@login_required
def return_book_view(request, pk):
    if not (request.user.role == 'admin' or request.user.role == 'faculty'):
        messages.error(request, "You do not have permission to manage returns.")
        return redirect('library')
        
    issue = get_object_or_404(BookIssue, pk=pk, return_date__isnull=True)
    
    if request.method == 'POST':
        issue.return_date = timezone.now().date()
        
        # Calculate fine (e.g., ₹1 per day late)
        if issue.return_date > issue.due_date:
            days_late = (issue.return_date - issue.due_date).days
            issue.fine_amount = days_late * 1.00 # 1 Rupee per day
            messages.warning(request, f"Book returned {days_late} days late. Fine of ₹{issue.fine_amount} applied.")
        
        issue.book.available_copies += 1
        issue.book.save()
        issue.save()
        
        messages.success(request, f"'{issue.book.title}' marked as returned.")
        return redirect('library')
    
    # If GET request, just show the confirmation
    context = {
        'issue': issue
    }
    return render(request, 'library/return_book_confirm.html', context)