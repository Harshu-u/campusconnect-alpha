# Inside: college_project/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure 'include' is here

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include your app's urls (now contains landing page at '' and dashboard at 'dashboard/')
    path('', include('core.urls')), 
    # Include Django's built-in auth URLs (handles login, logout, password reset etc.)
    path('registration/', include('django.contrib.auth.urls')), # <-- This is important
]