# --- File: students/urls.py ---
# This is the full and correct file.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_view, name='students'),
    path('add/', views.add_student_view, name='add_student'),
    path('edit/<int:pk>/', views.edit_student_view, name='edit_student'),     # <-- ADD THIS
    path('delete/<int:pk>/', views.delete_student_view, name='delete_student'), # <-- ADD THIS
]