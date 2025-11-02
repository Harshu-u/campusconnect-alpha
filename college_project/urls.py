from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views # Import core views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- FIXES ---
    # 1. Use our custom register view, named 'register'
    path('accounts/register/', core_views.register, name='register'),
    
    # 2. Use our custom logout view
    path('accounts/logout/', core_views.custom_logout, name='logout'),
    
    # 3. Include the rest of the default auth URLs (for login, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # --- END FIXES ---
    
    # Include URLs from all your apps
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('courses/', include('courses.urls')),
    path('timetable/', include('timetable.urls')),
    path('attendance/', include('attendance.urls')),
    path('exams/', include('exams.urls')),
    path('library/', include('library.urls')),
    path('fees/', include('fees.urls')),
    path('hostel/', include('hostel_transport.urls')),
    path('sports/', include('sports.urls')),

    # Core URLs (landing page, dashboard)
    path('', include('core.urls')), 
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)