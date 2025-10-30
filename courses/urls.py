from django.urls import path
from . import views 

urlpatterns = [
    path('', views.landing_view, name="landing"), 
    path('dashboard/', views.dashboard_view, name="dashboard"), 
    
    # ALL OTHER PATHS (students/, faculty/, etc.) ARE NOW REMOVED
]