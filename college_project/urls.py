# Inside: college_project/urls.py
from django.contrib import admin
from django.urls import path, include # Make sure 'include' is here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('accounts/', include('django.contrib.auth.urls')), # <-- ADD THIS LINE
]