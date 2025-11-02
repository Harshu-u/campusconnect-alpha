from django.urls import path
from . import views

urlpatterns = [
    # /students/
    path('', views.students_view, name='students'),
    
    # /students/add/
    path('add/', views.add_student_view, name='add_student'),
    
    # /students/edit/1/
    path('edit/<int:pk>/', views.edit_student_view, name='edit_student'),
    
    # /students/delete/1/
    path('delete/<int:pk>/', views.delete_student_view, name='delete_student'),
    
    # /students/import/
    path('import/', views.import_students_csv, name='import_students'),

    # /students/departments/
    path('departments/', views.department_list_view, name='departments'),
    
    # /students/departments/add/
    path('departments/add/', views.add_department_view, name='add_department'),
    
    # /students/departments/edit/1/
    path('departments/edit/<int:pk>/', views.edit_department_view, name='edit_department'),
    
    # /students/departments/delete/1/
    path('departments/delete/<int:pk>/', views.delete_department_view, name='delete_department'),
    
    # /students/departments/import/
    path('departments/import/', views.import_departments_csv, name='import_departments'),
]