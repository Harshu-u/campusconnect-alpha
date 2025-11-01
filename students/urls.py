# --- File: students/urls.py ---
# This is the full and correct file.

from django.urls import path
from . import views

urlpatterns = [
    path('', views.students_view, name='students'),
    path('add/', views.add_student_view, name='add_student'),
    path('edit/<int:pk>/', views.edit_student_view, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student_view, name='delete_student'),
    
    # URL for handling the Student CSV import
    path('import/', views.import_students_csv, name='import_students'),
    
    # NEW: URL for handling the Department CSV import
    path('import-departments/', views.import_departments_csv, name='import_departments'),

    # --- NEW DEPARTMENT CRUD URLS ---
    path('departments/', views.department_list_view, name='departments'),
    path('departments/add/', views.add_department_view, name='add_department'),
    path('departments/edit/<int:pk>/', views.edit_department_view, name='edit_department'),
    path('departments/delete/<int:pk>/', views.delete_department_view, name='delete_department'),
]