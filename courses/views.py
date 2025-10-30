from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# View for the public landing page
def landing_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')

# View for the dashboard (requires login)
@login_required
def dashboard_view(request):
    context = {} 
    return render(request, 'core/dashboard.html', context)

# View for registration
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # TODO: Add logic here to create the associated Student/Faculty profile
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})

# ALL OTHER VIEWS (students_view, faculty_view, etc.) MUST BE DELETED FROM THIS FILE