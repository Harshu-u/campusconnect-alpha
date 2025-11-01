# --- File: faculty/urls.py ---
# This is the full and correct file.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_view, name='faculty'),
    path('add/', views.add_faculty_view, name='add_faculty'),
    path('edit/<int:pk>/', views.edit_faculty_view, name='edit_faculty'),
    path('delete/<int:pk>/', views.delete_faculty_view, name='delete_faculty'),
    
    # NEW: URL for handling the CSV import
    path('import/', views.import_faculty_csv, name='import_faculty'),
]
