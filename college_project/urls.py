from django.contrib import admin
from django.urls import path, include
from core import views as core_views # Import core views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', core_views.register_view, name='register'),
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # 3. Include URLs from all your new apps
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('courses/', include('courses.urls')),       # <-- This is now correct
    path('timetable/', include('timetable.urls')),  # <-- ADD THIS
    path('attendance/', include('attendance.urls')),
    path('exams/', include('exams.urls')),
    path('library/', include('library.urls')),
    path('fees/', include('fees.urls')),
    path('hostel/', include('hostel_transport.urls')),
    path('sports/', include('sports.urls')),

    path('', include('core.urls')), 
]