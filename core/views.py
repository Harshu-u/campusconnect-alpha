from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm # Import our new form
from django.contrib import messages

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')

@login_required
def dashboard(request):
    # We'll add real data here later. For now, just render the template.
    context = {}
    return render(request, 'core/dashboard.html', context)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST) # Use our new form
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('dashboard')
        else:
            # Add error messages from the form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = RegistrationForm() # Use our new form
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('landing_page')