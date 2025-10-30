from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # To protect views

# View for the public landing page
def landing_view(request):
    # If the user is already logged in, redirect them to the dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'core/landing.html')

# View for the dashboard (requires login)
@login_required # This decorator ensures only logged-in users can see this
def dashboard_view(request):
    # You can add context data here later (e.g., counts for the cards)
    context = {} 
    return render(request, 'core/dashboard.html', context)

# Add placeholders for other views as we build them
@login_required
def students_view(request):
    # TODO: Add logic to fetch and display students
    context = {}
    return render(request, 'core/students.html', context)

@login_required
def faculty_view(request):
    # TODO: Add logic to fetch and display faculty
    context = {}
    return render(request, 'core/faculty.html', context)

@login_required
def courses_view(request):
    # TODO: Add logic to fetch and display courses
    context = {}
    return render(request, 'core/courses.html', context)

@login_required
def timetable_view(request):
    # TODO: Add logic for timetable
    # Pass days of week context if needed (JS might handle it now)
    context = {
        'days_of_week': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"] 
    }
    return render(request, 'core/timetable.html', context)

@login_required
def attendance_view(request):
    # TODO: Add logic for attendance
    from datetime import date
    context = {'today_date': date.today().strftime('%Y-%m-%d')}
    return render(request, 'core/attendance.html', context)

@login_required
def exams_view(request):
    # TODO: Add logic for exams
    context = {}
    return render(request, 'core/exams.html', context)

@login_required
def library_view(request):
    # TODO: Add logic for library
    context = {}
    return render(request, 'core/library.html', context)

@login_required
def fees_view(request):
    # TODO: Add logic for fees
    context = {}
    return render(request, 'core/fees.html', context)

@login_required
def hostel_view(request):
    # TODO: Add logic for hostel/transport
    context = {}
    return render(request, 'core/hostel.html', context)

@login_required
def sports_view(request):
    # TODO: Add logic for sports
    context = {}
    return render(request, 'core/sports.html', context)

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Save the new user
            
            # TODO: Add logic here to create the associated Student/Faculty profile
            # For now, we just create the User account
            
            login(request, user) # Log the user in
            return redirect('dashboard') # Redirect to the dashboard
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/register.html', {'form': form})

# Note: We don't need a specific view for login if using django.contrib.auth.urls
# Just ensure the template is in the right place.