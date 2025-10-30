from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Faculty

@login_required
def faculty_view(request):
    if not request.user.role == 'admin':
        return redirect('dashboard')
        
    faculty_list = Faculty.objects.select_related('user', 'department').all()
    context = {
        'faculty_list': faculty_list
    }
    return render(request, 'faculty/faculty.html', context)
