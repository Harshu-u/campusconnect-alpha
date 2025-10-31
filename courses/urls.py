from django.urls import path
from . import views 

app_name = 'courses' # <-- Add app_name

urlpatterns = [
    path('', views.courses_view, name="courses"), 
]