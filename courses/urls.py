# --- File: courses/urls.py ---
# This is the full and correct file.

from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Main course list view
    path('', views.course_list_view, name='courses'),
    
    # Add new course
    path('add/', views.add_course_view, name='add_course'),
    
    # Edit course
    path('edit/<int:pk>/', views.edit_course_view, name='edit_course'),
    
    # Delete course
    path('delete/<int:pk>/', views.delete_course_view, name='delete_course'),
]   