# --- File: courses/urls.py ---
# This is the full and correct file.

from django.urls import path
from . import views 

app_name = 'courses'

urlpatterns = [
    path('', views.courses_view, name="courses"), 
    path('add/', views.add_course_view, name='add_course'),
    path('edit/<int:pk>/', views.edit_course_view, name='edit_course'),     # <-- ADD THIS
    path('delete/<int:pk>/', views.delete_course_view, name='delete_course'), # <-- ADD THIS
]