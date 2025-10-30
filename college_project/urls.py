from django.contrib import admin
from django.urls import path, include
from core import views as core_views # Import core views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Handle Registration (from core.views)
    path('accounts/register/', core_views.register_view, name='register'),
    
    # 2. Handle auth (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # 3. Include URLs from all your new apps
    path('students/', include('students.urls')),
    path('faculty/', include('faculty.urls')),
    path('courses/', include('courses.urls')),
    path('attendance/', include('attendance.urls')),
    path('exams/', include('exams.urls')),
    path('library/', include('library.urls')),
    path('fees/', include('fees.urls')),
    path('hostel/', include('hostel_transport.urls')),
    path('sports/', include('sports.urls')),

    # 4. Handle core pages (landing, dashboard) LAST
    # This will match '' and 'dashboard/'
    path('', include('core.urls')), 
]