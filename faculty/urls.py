# --- File: faculty/urls.py ---
# This is the full and correct file (FIXED)

from django.urls import path
from . import views

urlpatterns = [
    # Path for the main faculty list view
    path('', views.faculty_view, name='faculty'),
    
    # Path for adding a new faculty member
    path('add/', views.add_faculty_view, name='add_faculty'),
    
    # Path for editing an existing faculty member (e.g., /faculty/edit/5/)
    path('edit/<int:pk>/', views.edit_faculty_view, name='edit_faculty'),
    
    # Path for deleting a faculty member (e.g., /faculty/delete/5/)
    path('delete/<int:pk>/', views.delete_faculty_view, name='delete_faculty'),
]