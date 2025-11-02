from django.urls import path
from . import views # Import views from the current directory (.)

urlpatterns = [
    # Use the landing_page view for the root URL
    path('', views.landing_page, name="landing_page"), 
    
    # Add a specific path for the dashboard
    path('dashboard/', views.dashboard, name="dashboard"), 
]